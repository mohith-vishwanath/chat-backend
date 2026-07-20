from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat Backend"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/chat_db"
    SECRET_KEY: str = "supersecretkey_please_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()
