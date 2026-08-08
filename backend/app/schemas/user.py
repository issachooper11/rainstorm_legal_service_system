from pydantic import BaseModel


# 接收前端传来的登录数据契约
class UserLogin(BaseModel):
    username: str
    password: str
