from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin
from app.crud.crud_user import get_user_by_username
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["认证"])


# 注意这里改成了 OAuth2PasswordRequestForm
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. 根据用户名去数据库查用户（OAuth2 表单里的字段叫 username）
    user = get_user_by_username(db, username=form_data.username)

    # 2. 校验用户和密码
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误"
        )

    # 3. 签发 Token
    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 这是一个受保护的接口，必须携带有效的 JWT 门票才能访问
@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "code": 200,
        "message": "验票成功，欢迎回来！",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            # 可以根据你的 user 模型字段按需返回，比如邮箱、角色等
        }
    }
