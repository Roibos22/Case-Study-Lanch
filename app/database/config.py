from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/lieferando_db"

    class Config:
        env_file = ".env"

db_settings = DatabaseSettings()