$ErrorActionPreference = "Stop"

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootDir

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Error "uv 未安装，请先安装 uv 后重试。"
  exit 1
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
  Write-Error "npm 未安装，请先安装 Node.js 与 npm 后重试。"
  exit 1
}

Write-Host "[INFO] 启动后端服务窗口..."
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$rootDir'; uv sync; uv run uvicorn app.main:app --reload"
)

Write-Host "[INFO] 启动前端服务窗口..."
Start-Process powershell -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$rootDir\SmartGuard-Vision-Fron'; npm install; npm run dev"
)

Write-Host "[INFO] 启动完成。"
Write-Host "[INFO] 前端地址: http://127.0.0.1:5173"
Write-Host "[INFO] 后端地址: http://127.0.0.1:8000"
