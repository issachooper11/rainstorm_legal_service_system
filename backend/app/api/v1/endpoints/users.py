from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.models.user import User

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
