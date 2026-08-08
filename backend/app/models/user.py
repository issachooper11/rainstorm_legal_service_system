from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
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
    # ➕ 新增字段
    real_name = Column(String(50), nullable=True)  # 真实姓名
    phone = Column(String(20), unique=True, index=True, nullable=True)  # 电话（加唯一和索引方便检索）
    email = Column(String(100), unique=True, index=True, nullable=True)  # 邮箱
    avatar = Column(String(255), nullable=True)  # 头像 URL 链接或相对路径

    # ➕ 审计时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 创建时间自动生成
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),
                        nullable=False)  # 更新时间自动刷新
