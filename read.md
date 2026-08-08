# Rainstorm Legal Service System (暴雨法律服务系统) 项目结构指南

本规范采用 **Vue 3 + Element Plus + FastAPI + Python + PostgreSQL** 现代全栈技术栈，遵循工业级“高内聚、低耦合”分层架构。

---

## 一、 后端项目 (`backend/`) 详细结构与作用

```text
backend/
├── app/                      # 后端核心源码总目录（内部子目录需带 __init__.py）
│   ├── __init__.py
│   ├── api/                  # 接口路由层（对接前端的 HTTP 入口）
│   │   ├── __init__.py
│   │   ├── v1/               # API 版本控制（规范化多版本迭代）
│   │   │   ├── __init__.py
│   │   │   ├── api.py        # 汇总注册所有子路由
│   │   │   └── endpoints/    # 各业务模块的具体路由逻辑
│   │   │       ├── __init__.py
│   │   │       ├── auth.py   # 登录、授权、Token 获取接口
│   │   │       └── cases.py  # 法律服务/案件管理模块接口
│   │   └── deps.py           # 公共依赖注入（如：获取数据库 Session、验证登录用户）
│   │
│   ├── core/                 # 全局核心配置层
│   │   ├── __init__.py
│   │   ├── config.py         # 使用 Pydantic 读取 .env 环境变量
│   │   └── database.py       # 配置 PostgreSQL 数据库连接引擎 (SQLAlchemy)
│   │
│   ├── crud/                 # 数据持久化/CRUD操作层（专门编写 SQL 交互和数据增删改查）
│   │   ├── __init__.py
│   │   └── crud_case.py      # 案件模块的具体数据库查询逻辑
│   │
│   ├── models/               # SQLAlchemy 数据模型层（对应 PostgreSQL 的表结构定义）
│   │   ├── __init__.py
│   │   └── case.py         # 定义数据库表、字段类型、主键约束
│   │
│   ├── schemas/              # Pydantic 数据验证与传输层（定义前后端交互的 JSON 契约）
│   │   ├── __init__.py
│   │   └── case.py         # 校验前端传参格式、规范后端返回数据结构
│   │
│   └── utils/                # 通用工具箱
│       ├── __init__.py
│       └── security.py       # 密码哈希加密、JWT Token 生成与校验
│
├── alembic/                  # PostgreSQL 数据库迁移版本控制目录（执行 alembic init 自动生成）
├── .env                      # 环境变量配置文件（存放数据库账号、密码、密钥，严禁提交到 Git）
├── requirements.txt          # Python 依赖包列表（如 fastapi, uvicorn, psycopg2, sqlalchemy）
└── main.py                   # FastAPI 应用总入口（启动服务、挂载 CORS 跨域中间件和路由）
```
---
## 二、 前端项目 (`frontend/`) 详细结构与作用

```text
frontend/
├── public/                   # 静态资源（不经过 Vite 编译打包，原样输出）
│   └── favicon.ico
│
├── src/                      # 前端源码主目录
│   ├── api/                  # 集中管理所有网络请求
│   │   ├── axios.js          # 封装 Axios 实例、统一拦截器（自动携带 Token、全局错误捕获）
│   │   └── case.js           # 法律服务/案件管理模块对应的后端接口调用函数
│   │
│   ├── assets/               # 静态资源存放处
│   │   └── styles/
│   │       └── global.css    # 全局公共样式与 CSS 变量
│   │
│   ├── components/           # 全局公共组件（多页面共用的小部件，如面包屑、弹窗等）
│   │
│   ├── router/               # 路由管理中心
│   │   └── index.js          # 定义 URL 路径与 Vue 页面的映射、登录拦截全局守卫
│   │
│   ├── store/                # Pinia 全局状态管理
│   │   └── user.js           # 存放当前登录用户的 Token、权限、基本信息
│   │
│   ├── views/                # 页面级组件（对应一个个具体的菜单功能页面）
│   │   ├── Login.vue         # 系统登录页
│   │   └── Case/             # 法律服务/案件管理模块
│   │       └── Index.vue     # 案件列表与操作主页面
│   │
│   ├── App.vue               # 根组件（整个前端应用的最外层容器）
│   └── main.js               # 主入口文件（挂载 Vue 实例、引入 Element Plus 和全局样式）
│
├── .env.development          # 开发环境变量（如：VITE_API_BASE_URL=http://localhost:8000/api）
├── .env.production           # 生产环境变量
├── package.json              # 前端项目依赖与运行脚本户口本
└── vite.config.js            # Vite 构建配置文件（配置代理解决跨域、配置 `@` 路径别名）
```