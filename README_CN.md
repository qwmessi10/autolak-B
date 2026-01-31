# AutoLak 网站项目 - README (中文版)

## 1. 项目结构

*   **backend/**: Django 后端
    *   `autolak_backend/`: 核心设置和 URL 路由。
    *   `users/`: 用户认证、余额和个人资料逻辑。
    *   `orders/`: 订单处理和 Telegram 集成。
    *   `content/`: 首页内容、FAQ、SEO 文章配置。
*   **frontend/**: Vue 3 前端
    *   `src/pages/`: 页面组件 (首页, 登录, 注册, 订单, 管理员后台, SEO 课程)。
    *   `src/stores/`: Pinia 状态管理 (认证信息)。

## 2. 安装与运行指南

### 前置要求
*   Python 3.10+
*   Node.js 16+
*   MySQL Server (本地运行)

### 后端设置（不使用虚拟环境）
1.  进入后端文件夹：
    ```powershell
    cd backend
    ```
2.  全局（或用户级）安装依赖：
    ```powershell
    pip install -r requirements.txt
    # 如果没有 pip 命令：
    python -m pip install -r requirements.txt
    ```
3.  数据库设置：
    ```powershell
    # 确保 MySQL 运行，用户名 root 密码 root
    # 数据库 autolak 存在（如未创建请自行创建）
    python manage.py migrate
    ```
4.  创建管理员账号（可选）：
    ```powershell
    python manage.py createsuperuser
    # 用户名: admin
    # 邮箱: admin@example.com
    # 密码: zw20181227
    ```
5.  运行服务器：
    ```powershell
    python manage.py runserver
    ```
    *   API 地址: `http://localhost:8000`

### 使用 Ngrok 暴露本地后端（供 Vercel 前端访问）
- 下载并安装： https://ngrok.com/download
- 登录授权（仅一次）：
  ```powershell
  ngrok config add-authtoken <你的NGROK_TOKEN>
  ```
- 启动隧道（把本地后端 8000 端口暴露到公网）：
  ```powershell
  ngrok http 8000
  ```
- 复制生成的公网地址（例如 `https://xxxx-xxxx.ngrok-free.dev`）
- 在 Vercel → 项目 → Settings → Environment Variables：
  - 设置 `VITE_API_URL` = `https://xxxx-xxxx.ngrok-free.dev`
  - 点击 Redeploy 重新部署前端，使环境变量生效
- 后端安全说明：
  - 已允许 CORS 和 `ngrok-skip-browser-warning` 头
  - 建议将你的 Vercel 域名加入 `CSRF_TRUSTED_ORIGINS`（例如 `https://your-project.vercel.app`）
  - 免费版 ngrok 域名每次重启都会变化，请更新 `VITE_API_URL` 并重新部署前端

### 前端设置 (Frontend)
1.  进入前端文件夹：
    ```powershell
    cd frontend
    ```
2.  安装依赖：
    ```powershell
    npm install
    ```
3.  运行开发服务器：
    ```powershell
    npm run dev
    ```
    *   网站地址: `http://localhost:5173`

## 3. 图片资源管理

您可以将自定义图片放在 `backend/media/` 目录下，或者通过管理员后台直接上传。

*   **首页图片**:
    *   进入 **Admin Panel (管理员后台)** -> **Site Content (站点内容)**。
    *   上传 Slogan 背景图、Intro 流程图和成功案例图片。
    *   后端会自动将它们保存到 `backend/media/homepage/` 和 `backend/media/cases/` 目录。
*   **注意**:
    *   如果你没有在后台上传图片，前端会默认使用占位图。
    *   确保后端 `settings.py` 中的 `MEDIA_URL` 和 `MEDIA_ROOT` 配置正确（已配置）。

## 4. 核心功能说明

*   **管理员后台**: 使用 `admin` / `zw20181227` 登录。
    *   **Site Content**: 编辑首页文本（Slogan, Intro, Cases）、FAQ 和图片。
    *   **System Config**: 设置 Telegram Bot Token 和 Chat ID 用于订单通知。
    *   **SEO Class**: 撰写和管理 SEO 文章 (支持 Markdown 语法)。
    *   **User Management**: 查看用户列表，修改用户余额，管理用户任务 (设置状态/失败原因)。
*   **Telegram 集成**:
    *   在 Admin -> System Config 中配置您的 Bot Token 和 Group ID。
    *   新订单会自动推送到指定的 Telegram 群组。
*   **风控系统**:
    *   同一个用户名/邮箱不能重复注册。
    *   同一个设备 (基于 Cookie 识别) 无法注册多个账号。
