#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "[ERROR] uv 未安装，请先安装 uv 后重试。"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "[ERROR] npm 未安装，请先安装 Node.js 与 npm 后重试。"
  exit 1
fi

echo "[INFO] 启动后端服务..."
(
  uv sync
  uv run uvicorn app.main:app --reload
) &
BACKEND_PID=$!

echo "[INFO] 启动前端服务..."
(
  cd SmartGuard-Vision-Fron
  npm install
  npm run dev -- --host 0.0.0.0
) &
FRONTEND_PID=$!

cleanup() {
  echo ""
  echo "[INFO] 正在停止服务..."
  kill "$BACKEND_PID" "$FRONTEND_PID" >/dev/null 2>&1 || true
}

trap cleanup INT TERM EXIT

echo "[INFO] 启动完成。"
echo "[INFO] 前端地址: http://127.0.0.1:5173"
echo "[INFO] 后端地址: http://127.0.0.1:8000"

wait "$BACKEND_PID" "$FRONTEND_PID"
