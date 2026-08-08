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
    is_active: Optional[bool] = Field(True, description="是否激活")
    role: int = Field(3, ge=1, le=5, description="角色: 1-主任, 2-合伙人, 3-律师, 4-助理, 5-系统管理员")
