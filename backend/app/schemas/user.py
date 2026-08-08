from typing import Optional

from pydantic import BaseModel, Field


# 1. 登录数据契约（保持不变，用于校验登录时的账号密码）
class UserLogin(BaseModel):
    username: str = Field(..., description="登录账号/用户名")
    password: str = Field(..., description="登录密码")


# 2. 创建团队账号契约（已集成新增的：真实姓名、电话、邮箱、头像）
class UserCreate(BaseModel):
    username: str = Field(..., description="用户名（登录账号）")
    password: str = Field(..., description="密码")

    # 基础与权限字段
    is_active: Optional[bool] = Field(True, description="是否激活")
    role: int = Field(3, ge=1, le=5, description="角色: 1-董事长, 2-合伙人, 3-律师, 4-助理, 5-系统管理员")

    # ➕ 新增字段
    real_name: Optional[str] = Field(None, description="真实姓名")
    phone: Optional[str] = Field(None, description="电话号码")
    email: Optional[str] = Field(None, description="电子邮箱")
    avatar: Optional[str] = Field(None, description="头像URL")
