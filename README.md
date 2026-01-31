# AutoLak Website Project - README

## 1. Project Structure

*   **backend/**: Django Backend
    *   `autolak_backend/`: Core settings and URLs.
    *   `users/`: User authentication, balance, and profile logic.
    *   `orders/`: Order processing and Telegram integration.
    *   `content/`: Homepage content, FAQs, SEO articles configuration.
*   **frontend/**: Vue 3 Frontend
    *   `src/pages/`: Page components (Home, Login, Register, Order, Admin, SEO Class).
    *   `src/stores/`: Pinia state management (Auth).

## 2. Setup & Run Instructions

### Prerequisites
*   Python 3.10+
*   Node.js 16+
*   MySQL Server (Running locally)

### Backend Setup (No Virtual Environment)
1.  Navigate to the backend folder:
    ```powershell
    cd backend
    ```
2.  Install dependencies globally (or user level):
    ```powershell
    pip install -r requirements.txt
    # If pip not found, use:
    python -m pip install -r requirements.txt
    ```
3.  Database Setup:
    ```powershell
    # Ensure MySQL is running (user: root, password: root)
    # Create database 'autolak' if not exists
    python manage.py migrate
    ```
4.  Create Admin User (optional):
    ```powershell
    python manage.py createsuperuser
    # Username: admin
    # Email: admin@example.com
    # Password: zw20181227
    ```
5.  Run Server:
    ```powershell
    python manage.py runserver
    ```
    *   API runs at: `http://localhost:8000`

### Ngrok Tunnel (Expose Backend to Vercel)
- Install Ngrok: https://ngrok.com/download
- Authenticate (once):
  ```powershell
  ngrok config add-authtoken <YOUR_NGROK_TOKEN>
  ```
- Start tunnel for backend:
  ```powershell
  ngrok http 8000
  ```
- Copy the public URL (e.g. `https://xxxx-xxxx.ngrok-free.dev`)
- In Vercel → Project → Settings → Environment Variables:
  - Set `VITE_API_URL` = `https://xxxx-xxxx.ngrok-free.dev`
  - Redeploy the frontend to apply
- Backend security notes:
  - We already allow CORS and the `ngrok-skip-browser-warning` header
  - Add your Vercel domain to `CSRF_TRUSTED_ORIGINS` (e.g. `https://your-project.vercel.app`)
  - Free ngrok domains change on restart; update `VITE_API_URL` and redeploy when it changes

### Frontend Setup
1.  Navigate to the frontend folder:
    ```powershell
    cd frontend
    ```
2.  Install Dependencies:
    ```powershell
    npm install
    ```
3.  Run Development Server:
    ```powershell
    npm run dev
    ```
    *   Website runs at: `http://localhost:5173`

## 3. Image Assets Management

You can place your custom images in `backend/media/` directory or upload them directly via the Admin Panel.

*   **Homepage Images**:
    *   Go to Admin Panel -> Site Content.
    *   Upload images for Slogan background, Intro flowchart, and Success Cases.
    *   Backend will automatically save them to `backend/media/homepage/` and `backend/media/cases/`.

## 4. Key Features Guide

*   **Admin Panel**: Login with `admin` / `zw20181227`.
    *   **Site Content**: Edit homepage texts, FAQs, and images.
    *   **System Config**: Set Telegram Bot Token and Chat ID for order notifications.
    *   **SEO Class**: Write and manage SEO articles (Markdown supported).
    *   **User Management**: View users, modify balances, manage tasks (set status/fail reason).
*   **Telegram Integration**:
    *   Configure your Bot Token and Group ID in Admin -> System Config.
    *   New orders are automatically sent to the Telegram group.
*   **Risk Control**:
    *   Same username/email cannot register twice.
    *   Same device (cookie-based) cannot register multiple accounts.
