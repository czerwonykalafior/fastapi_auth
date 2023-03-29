from fastapi import FastAPI

from auth.authentication import authentication_router
from endpoints import core_router

app = FastAPI()
app.include_router(authentication_router)
app.include_router(core_router)
