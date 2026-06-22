import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    QWEN_API_KEY = os.getenv("QWEN_API_KEY")

settings = Settings()