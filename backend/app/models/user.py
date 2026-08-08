from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 绝不存明文密码
    is_active = Column(Boolean, server_default="true", nullable=False)
    # 增加角色字段
    # chairman 主任、partner 合伙人、lawyer 执业律师、assistant 律师助理、admin_staff 行政
    role = Column(String, server_default="lawyer", nullable=False)
