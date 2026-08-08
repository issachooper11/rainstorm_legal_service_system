from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Pydantic 会自动去 .env 文件中寻找同名字段
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 实例化一个全局配置对象，供其他文件直接引入
settings = Settings()
