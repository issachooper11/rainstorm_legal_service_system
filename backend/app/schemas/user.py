from typing import Optional

from pydantic import BaseModel, Field


# 接收前端传来的登录数据契约
class UserLogin(BaseModel):
    username: str
    password: str


# 创建团队账号
class UserCreate(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    role: str = Field(..., description="角色: partner, lawyer, assistant, admin_staff")
    is_active: Optional[bool] = Field(True, description="是否激活")
