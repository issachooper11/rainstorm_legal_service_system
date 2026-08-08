from fastapi import FastAPI
from app.api.v1.endpoints import auth, users

app = FastAPI(title="Rainstorm Legal Service System")

# 挂载认证路由，并加上统一前缀 /api/v1
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to Rainstorm Legal Service System API"}
