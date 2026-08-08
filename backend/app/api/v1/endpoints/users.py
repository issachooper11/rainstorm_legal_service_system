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


# 2. 【新增】创建/注册新用户接口
@router.post("/", dependencies=[Depends(require_roles([1, 2, 5]))])  # ➕ 优化点1：允许 1(董事长)、2(合伙人)、5(管理员) 创建用户
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已经存在
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已存在"
        )

    # （可选扩展）检查电话或邮箱是否已被占用
    if user_in.phone:
        existing_phone = db.query(User).filter(User.phone == user_in.phone).first()
        if existing_phone:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该电话号码已被注册")

    if user_in.email:
        existing_email = db.query(User).filter(User.email == user_in.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该邮箱已被注册")

    # 密码加密
    hashed_password = get_password_hash(user_in.password)

    # ➕ 优化点2：创建用户对象时，完整接收并传入新增的字段
    new_user = User(
        username=user_in.username,
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=user_in.is_active,
        real_name=user_in.real_name,
        phone=user_in.phone,
        email=user_in.email,
        avatar=user_in.avatar
    )

    # 写入数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ➕ 优化点3：返回数据中把新增字段带上，方便前端即时展示
    return {
        "code": 200,
        "message": "用户创建成功",
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role,
            "is_active": new_user.is_active,
            "real_name": new_user.real_name,
            "phone": new_user.phone,
            "email": new_user.email,
            "avatar": new_user.avatar,
            "created_at": new_user.created_at,
            "updated_at": new_user.updated_at
        }
    }
