from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 绝不存明文密码
    is_active = Column(Boolean, server_default="true", nullable=False)
    # 增加角色字段
    # 角色: 1-主任(chairman), 2-合伙人(partner), 3-律师(lawyer), 4-助理(assistant), 5-系统管理员(admini)
    role = Column(Integer, default=3, nullable=False, comment="用户角色类型(1-5)")
