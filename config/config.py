import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_URL = os.getenv("DB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "test")
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
ALGORITHM = "HS256"

# Email Configuration
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "example@example.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "password")
MAIL_FROM = os.getenv("MAIL_FROM", "example@example.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "100"))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.example.com")

#FE URL
URL_VERIFY_EMAIL = os.getenv("URL_VERIFY_EMAIL", "localhost:8000")
