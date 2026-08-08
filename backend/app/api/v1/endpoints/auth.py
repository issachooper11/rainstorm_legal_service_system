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
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    # 1. 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()

    # 2. 校验账号密码是否正确
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误"
        )

    # 3. 【关键新增】校验账号是否被停用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您的账号已被停用，请联系律所管理员"
        )

    # 4. 生成 Token 并返回
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
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
