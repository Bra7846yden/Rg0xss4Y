# 代码生成时间: 2025-08-28 11:24:00
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Request, Status
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from starlette.middleware.sessions import SessionMiddleware, SessionBackend
from starlette.middleware.sessions import SessionDisallowed
from starlette.status import HTTP_401_UNAUTHORIZED
import secrets
import json

# 假设的用户数据库
USERS = {
    "user1": "password1",
    "user2": "password2"
}

# 简单的密码验证函数
def check_password(username, password):
    """
    验证用户名和密码是否正确。
    """
    return USERS.get(username) == password

# 登录视图函数
async def login(request: Request):
    """
    处理用户登录请求。
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return JSONResponse(
            content={"error": "Missing username or password"},
            status_code=Status.BAD_REQUEST
        )
    if check_password(username, password):
        session_id = secrets.token_hex(16)
        # 将用户名存储在会话中
        await request.session.set("user\,id", username)
        return JSONResponse(
            content={"message": "Login successful", "session_id": session_id},
            status_code=Status.OK
        )
    else:
        return JSONResponse(
            content={"error": "Invalid username or password"},
            status_code=Status.UNAUTHORIZED
        )

# 受保护的视图函数
@requires("authenticated")
async def protected_view(request: Request):
    """
    一个需要认证的视图。
    """
    user_id = request.session.get("user\,id")
    return JSONResponse(
        content={"message": f"You are logged in as {user_id}"},
        status_code=Status.OK
    )

# 创建Starlette应用
app = Starlette(
    routes=[
        Route("/login", login, methods=["POST"]),
        Route("/protected", protected_view, methods=["GET"]),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key="your_secret_key"),
    ],
)

# 错误处理
@app.exception_handler(SessionDisallowed)
async def session_disallowed(request, exc):
    return JSONResponse(
        content={"error": "Session middleware is disabled"},
        status_code=HTTP_401_UNAUTHORIZED
    )

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
