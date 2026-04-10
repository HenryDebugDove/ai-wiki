@echo off
echo ====================================
echo NestJS 演示项目 - 快速启动脚本
echo ====================================
echo.

echo [1/3] 检查依赖...
if not exist "node_modules" (
    echo 依赖未安装，正在安装...
    call npm install
    echo.
) else (
    echo 依赖已安装
    echo.
)

echo [2/3] 启动开发服务器...
echo 服务器将在 http://localhost:3000 上运行
echo 按 Ctrl+C 停止服务器
echo.

call npm run start:dev

pause
