from fastapi import FastAPI
from routes import auth
from contextlib import asynccontextmanager
from database.connection import close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database connection is established when module is imported
    yield
    close_mongo_connection()


app = FastAPI(lifespan=lifespan)
app.include_router(auth.auth_router)
