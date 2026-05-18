from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/fakeshield"

    # Email alerts
    ALERT_EMAIL_ENABLED: bool = False   # set True when ready
    ALERT_EMAIL_TO:      str  = "admin@yourproject.com"
    SMTP_HOST:           str  = "smtp.gmail.com"
    SMTP_PORT:           int  = 587
    SMTP_USER:           str  = ""
    SMTP_PASSWORD:       str  = ""
    SMTP_FROM:           str  = "fakeshield@yourproject.com"

    # App
    ENVIRONMENT: str = "development"
    API_PORT:    int = 8001

    # Optional development configs
    HF_TOKEN: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL:   str = ""
    PORT:     int = 8000
    DEBUG:    bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
