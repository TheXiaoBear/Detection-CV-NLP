from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    # mysql
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    # redis
    REDIS_HOST: str
    REDIS_PORT: int

    # rabbitmq
    MQ_HOST: str
    MQ_PORT: int
    MQ_USERNAME: str
    MQ_PASSWORD: str

    # jwt
    JWT_SECRET: str

    # oss
    OSS_ACCESS_KEY_ID: str
    OSS_ACCESS_KEY_SECRET: str

    OSS_ENDPOINT: str
    OSS_REGION: str

    OSS_BUCKET: str
    OSS_DOMAIN: str

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()