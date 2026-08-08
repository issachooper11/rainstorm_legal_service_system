from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建数据库连接引擎
engine = create_engine(settings.DATABASE_URL)

# 创建本地会话工厂（用于后续增删改查时开启数据库会话）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据库模型的基类（我们前面写的 User 模型就要继承它）
Base = declarative_base()


# 获取数据库会话的依赖函数（后续会用在 FastAPI 的 Depends 中）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
