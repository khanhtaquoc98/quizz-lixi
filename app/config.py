import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "Ai Được Lì Xì - Đố Vui Trí Tuệ AI"
    BASE_DIR: Path = BASE_DIR
    
    # Groq AI Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_API_KEY_CHAT_BOT: str = os.getenv("GROQ_API_KEY_CHAT_BOT", "").strip()
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b").strip()
    
    # Telegram Notifications
    CRON_SECRET: str = os.getenv("CRON_SECRET", "daily_notification").strip()
    NOTI_CHAT_ID: str = os.getenv("NOTI_CHAT_ID", "-1001505319885").strip()
    NOTI_TOPIC_ID: str = os.getenv("NOTI_TOPIC_ID", "61684").strip()
    SUMMARY_TOPIC_ID: str = os.getenv("SUMMARY_TOPIC_ID", "61684").strip()
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    
    # Server Settings
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

settings = Settings()
