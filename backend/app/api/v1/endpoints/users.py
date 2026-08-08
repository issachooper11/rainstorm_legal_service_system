from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

router = APIRouter(prefix="/users", tags=["用户管理"])


# 只有 role 为 "partner" 的合伙人才能访问这个接口
@router.get("/", dependencies=[Depends(require_roles(["partner"]))])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {
        "code": 200,
        "message": "获取用户列表成功",
        "data": users
    }


# 2. 【新增】创建/注册新用户接口（只有 partner 可以操作）
@router.post("/", dependencies=[Depends(require_roles(["partner"]))])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已经存在
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已存在"
        )

    # 密码加密
    hashed_password = get_password_hash(user_in.password)

    # 创建用户对象
    new_user = User(
        username=user_in.username,
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=user_in.is_active
    )

    # 写入数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "code": 200,
        "message": "用户创建成功",
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role,
            "is_active": new_user.is_active
        }
    }
