from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_port: int = 8000

    mongo_root_user: str = "admin"
    mongo_root_password: str = "changeme"
    mongo_db: str = "esg_db"
    mongo_host: str = "mongo"
    mongo_port: int = 27017

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def mongo_uri(self) -> str:
        return (
            f"mongodb://{self.mongo_root_user}:{self.mongo_root_password}"
            f"@{self.mongo_host}:{self.mongo_port}/?authSource=admin"
        )


settings = Settings()
