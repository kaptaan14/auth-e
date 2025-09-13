from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from service import auth
from schema import User

router = APIRouter()
auth_router = APIRouter(prefix="/v1/auth")

@auth_router.post("/register")
async def register(request_body: User):
    return await auth.register_user(request_body)


@auth_router.post("/verify-email")
async def verify_email(token: str):
    return await auth.verify_email(token)


@auth_router.post("/login")
async def login(request_body: User, response: Response):
    return await auth.login(request_body, response)
