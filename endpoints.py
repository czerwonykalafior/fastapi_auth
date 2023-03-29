from fastapi import APIRouter, Depends, Security
from typing_extensions import Annotated

from auth.authorization import get_current_active_user, get_current_user
from auth.models import User

core_router = APIRouter()


@core_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@core_router.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])]):
    return [{"item_id": "Foo", "owner": current_user.username}]


@core_router.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}
