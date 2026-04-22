@echo off
setlocal

set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

where uv >nul 2>nul
if errorlevel 1 (
  echo [ERROR] uv 未安装，请先安装 uv 后重试。
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo [ERROR] npm 未安装，请先安装 Node.js 与 npm 后重试。
  exit /b 1
)

echo [INFO] 启动后端服务窗口...
start "SmartGuard Backend" cmd /k "cd /d %ROOT_DIR% && uv sync && uv run uvicorn app.main:app --reload"

echo [INFO] 启动前端服务窗口...
start "SmartGuard Frontend" cmd /k "cd /d %ROOT_DIR%SmartGuard-Vision-Fron && npm install && npm run dev"

echo [INFO] 启动完成。
echo [INFO] 前端地址: http://127.0.0.1:5173
echo [INFO] 后端地址: http://127.0.0.1:8000
