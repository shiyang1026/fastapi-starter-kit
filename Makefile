# 默认端口 8000，如果环境变量 PORT 有值则用环境变量
PORT := 8000

.PHONY: dev
dev:
	uv run fastapi dev app/main.py --port $(PORT)

.PHONY: run
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

# --- Database Migrations ---
.PHONY: migration
migration:
	# 生成迁移文件 (usage: make migration msg="add user table")
	uv run alembic revision --autogenerate -m "$(msg)"

.PHONY: migrate
migrate:
	# 执行迁移，应用到数据库
	uv run alembic upgrade head

.PHONY: downgrade
downgrade:
	# 回滚上一次迁移
	uv run alembic downgrade -1

# --- Docker Compose Infrastructure ---
ENV_FILE := .env.dev

.PHONY: infra-up
infra-up:
	# 启动本地开发依赖 (DB & Redis)
	docker compose --env-file $(ENV_FILE) -f docker-compose-dev.yaml up -d

.PHONY: infra-down
infra-down:
	# 停止依赖
	docker compose --env-file $(ENV_FILE) -f docker-compose-dev.yaml down

.PHONY: infra-logs
infra-logs:
	# 查看依赖日志
	docker compose --env-file $(ENV_FILE) -f docker-compose-dev.yaml logs -f

# --- Code Quality ---
.PHONY: lint
lint:
	# 检查代码风格
	uv run ruff check .

.PHONY: format
format:
	# 格式化代码
	uv run ruff check --fix .
	uv run ruff format .