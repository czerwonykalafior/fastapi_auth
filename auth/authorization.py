from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
from starlette import status
from typing_extensions import Annotated

from auth.authentication import ALGORITHM, SECRET_KEY
from auth.models import TokenData, User
from db import fake_users_db, get_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


def validate_token(token: str) -> TokenData:
    jwt_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = jwt_payload.get("sub")

    if username is None:
        raise ValidationError('Username not in "sub".')

    token_scopes = jwt_payload.get("scopes", [])
    token_data = TokenData(scopes=token_scopes, username=username)

    return token_data


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        token_data = validate_token(token)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=["me"])]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
