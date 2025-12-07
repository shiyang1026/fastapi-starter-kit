[English](README_en.md) | [中文](README.md)

# FastAPI Starter Kit

这是一个基于 FastAPI 的现代化后端启动模板，旨在提供高性能、易扩展且开发体验友好的基础架构。本项目集成了主流的 Python 异步生态工具，帮助开发者快速构建生产级别的 Web 应用。

## 特性

本项目精选了以下技术栈和工具：

- **Web 框架**: FastAPI (高性能异步框架)
- **数据库 ORM**: SQLModel (结合 SQLAlchemy 和 Pydantic 的现代化 ORM)
- **数据库迁移**: Alembic (轻量级数据库版本控制)
- **异步驱动**: asyncpg (PostgreSQL)
- **缓存**: Redis (支持异步操作)
- **认证与安全**:
  - PyJWT (JSON Web Token 处理)
  - Pwdlib (密码哈希与校验，使用 Argon2)
- **依赖管理**: uv (极速 Python 包与项目管理器)
- **代码质量**: Ruff (极速代码分析与格式化工具)

## 快速开始

请按照以下步骤快速启动本地开发环境。

### 前置要求

确保本地已安装以下工具：
- Python 3.12+
- Docker & Docker Compose
- uv (推荐用于依赖管理)

### 1. 初始化项目依赖

安装项目所需的 Python 依赖：

```bash
uv sync
```

### 2. 启动基础服务

使用 Docker Compose 启动 PostgreSQL 和 Redis 服务：

```bash
make infra-up
```

### 3. 数据库迁移

应用数据库迁移以创建表结构：

```bash
make migrate
```

### 4. 启动开发服务器

### 5. 代码质量检查

本项目使用 Ruff 进行代码检查和格式化，这也是现代 Python 开发的标准工具。由于它已包含在项目的开发依赖中，你无需手动安装，直接通过 `uv` 或 `make` 运行即可。

运行代码检查：
```bash
make lint
```

自动格式化代码：
```bash
make format
```

```bash
make dev
```

服务启动后，可以访问以下地址：
- API 文档 (Swagger UI): http://127.0.0.1:8000/docs
- API 文档 (ReDoc): http://127.0.0.1:8000/redoc

## 常用命令

本项目提供了 `Makefile` 简化常用操作：

- `make run`: 启动生产环境服务器 (Uvicorn)
- `make dev`: 启动开发环境服务器
- `make infra-up`: 启动依赖服务 (DB, Redis)
- `make infra-down`: 停止依赖服务
- `make migration msg="描述"`: 生成新的数据库迁移脚本
- `make migrate`: 执行数据库迁移
- `make downgrade`: 回滚上一次迁移
- `make lint`: 运行代码检查 (Ruff)
- `make format`: 自动格式化代码 (Ruff)


## 数据库迁移流程

新增数据表时的标准流程：

1. **定义模型**: 在 `app/models/` 下创建新的模型文件（或在现有文件中添加）。
2. **注册模型**: **关键步骤！** 必须在 `alembic/env.py` 中导入新定义的模型，否则 Alembic 无法检测到变更。
   ```python
   # alembic/env.py
   from app.models.new_model import NewModel  # noqa
   ```
3. **生成迁移**:
   ```bash
   make migration msg="add new model"
   ```
4. **检查迁移脚本**: 检查 `alembic/versions/` 下生成的 Python 脚本是否正确。
5. **应用迁移**:
   ```bash
   make migrate
   ```

```bash
make dev
```

```
app/
├── api/          # API 路由定义 (Endpoints)
├── core/         # 核心配置 (Config, Security, Events)
├── db/           # 数据库连接与 Session 管理
├── models/       # SQLModel 数据模型定义
├── schemas/      # Pydantic 数据验证模型 (Request/Response)
├── services/     # 复杂业务逻辑层
└── main.py       # 应用入口文件
```
