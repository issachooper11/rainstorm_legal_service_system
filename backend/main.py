from fastapi import FastAPI
from app.api.v1.endpoints import auth, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rainstorm Legal Service System")

# 挂载认证路由，并加上统一前缀 /api/v1
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端来源，生产环境可以写具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to Rainstorm Legal Service System API"}
