from database.connection import db
from fastapi import HTTPException, Response
from datetime import datetime, timezone, timedelta
from schema import User
import uuid
from fastapi_mail import FastMail, MessageSchema
from jose import jwt
from config.constants import mail_config
from config.config import SECRET_KEY, ALGORITHM, URL_VERIFY_EMAIL
from passlib.context import CryptContext


def get_password_hash(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_user(request_body: User):
    email = request_body.email
    password = request_body.password
    
    # Validate password length
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    if await db.users.find_one({"email": email}):
            raise HTTPException(status_code=400, detail="Email already registered")


    verification_token = str(uuid.uuid4())
    hashed_password = get_password_hash(password)
    
    user = {
        "email": email,
        "password": hashed_password,
        "is_verified": False,
        "verification_token": verification_token,
        "created_at": datetime.now(timezone.utc)
    }

    await db.users.insert_one(user)

    verification_link = f"{URL_VERIFY_EMAIL}/?token={verification_token}"
    
    with open("templates/verify_email.html", "r") as file:
        html_template = file.read()
    
    # Replace placeholders in template
    html_content = html_template.replace("{{ verification_link }}", verification_link).replace("{{ email }}", email)
    
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=html_content,
        subtype="html"
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)

    return {"message": "Registration successful, please verify your email."}

    
async def verify_email(token: str):
    user = await db.users.find_one({"verification_token": token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"is_verified": True}, "$unset": {"verification_token": ""}}
    )
    return {"message": "Email verified successfully! You can now login."}


async def login(request_body: User, response: Response):
    email = request_body.email
    password = request_body.password

    user = await db.users.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=400, detail="User not registered")

    if not user.get("is_verified", False):
        raise HTTPException(status_code=400, detail="Please verify your email before logging in")

    if not verify_password(password, user.get("password")):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token_expires = timedelta(minutes=60*24*30)
    access_token = create_access_token(
        data={"sub": user["email"], "email": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60*24*30
    )

    return {"message": "Login successful", "data": {"email": user.get("email"), "token": access_token}}