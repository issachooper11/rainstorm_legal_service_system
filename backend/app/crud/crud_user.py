from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_username(db: Session, username: str):
    # 使用 SQLAlchemy 查询 users 表中是否存在该用户名
    return db.query(User).filter(User.username == username).first()
