import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

settings = Settings()