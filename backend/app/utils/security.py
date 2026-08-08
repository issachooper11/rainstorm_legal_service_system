from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 密码加密上下文（使用 bcrypt 算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 1. 验证密码是否正确（核心修改：这里也必须做 72 字节截断！）
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(password_bytes.decode('utf-8', errors='ignore'), hashed_password)


# 2. 将明文密码加密
def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes.decode('utf-8', errors='ignore'))


# 3. 生成 JWT Token（登录成功后发门票）
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
