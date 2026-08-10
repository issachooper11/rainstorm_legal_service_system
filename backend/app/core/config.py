import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---------------- 1. 基础与安全配置 ----------------
    APP_NAME: str = "rainstorm_legal_service_system"
    DATABASE_URL: str
    SECRET_KEY: str = "your-default-secret-key"

    # ---------------- 2. 邮件与服务配置 ----------------
    SMTP_SERVER: str = "smtp.163.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SENDER_NAME: str = "觅理常法"

    # ---------------- 3. 动态路径配置（自动计算，精准定位） ----------------
    # BASE_DIR: current_file -> app/core/config.py -> parent(core) -> parent(app) -> parent(backend)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # APP_DIR: backend/app/ 目录
    APP_DIR: Path = BASE_DIR / "app"

    # ASSETS_DIR: backend/app/assets/ 目录
    ASSETS_DIR: Path = APP_DIR / "assets"

    # 静态文件快捷访问属性
    @property
    def CHECKLIST_POSTER_PATH(self) -> Path:
        """法律体检清单图片路径 (backend/app/assets/觅理-企业法律体检清单.png)"""
        return self.ASSETS_DIR / "觅理-企业法律体检清单.png"

    @property
    def PRODUCT_MANUAL_PATH(self) -> Path:
        """常法产品手册 PDF 路径 (backend/app/assets/觅理-常法产品手册.pdf)"""
        return self.ASSETS_DIR / "觅理-常法产品手册.pdf"

    # ---------------- 4. 环境变量配置文件定位 ----------------
    # 动态定位到 backend/.env 文件，解决命令行启动路径不同导致找不到 .env 的问题
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# 实例化一个全局配置对象，供其他模块（如 email service, api endpoints 等）直接引入
settings = Settings()
