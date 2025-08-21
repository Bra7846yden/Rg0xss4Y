# 代码生成时间: 2025-08-21 23:22:17
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Request, Response
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware, AuthenticationBackend, SimpleUser, requires
from starlette.middleware.sessions import SessionMiddleware
from starlette.datastructures import Secret

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

# 模拟的用户数据库
users_db = {
    "username": "admin",
    "password": "password123"
}

# JWT Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")

class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request) -> Optional[SimpleUser]:
        # 从请求头中获取JWT Token
        token = request.headers.get("Authorization")
        if token is None:
            return None
        # 验证JWT Token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return SimpleUser(payload["username"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def login(request: Request) -> Response:
    # 获取请求体中的用户名和密码
    username = request.form["username"]
    password = request.form["password"]
    # 验证用户
    if username == users_db["username"] and password == users_db["password"]:
        # 生成JWT Token
        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return JSONResponse(
            {
                "username": username,
                "token": token
            },
            status_code=HTTP_200_OK
        )
    else:
        return JSONResponse(
            {"detail": "Incorrect username or password"},
            status_code=HTTP_400_BAD_REQUEST
        )

# 路由配置
routes = [
    Route("/login", endpoint=login, methods=["POST"]),
]

# 应用配置
app = Starlette(
    middleware=[
        # 会话中间件
        SessionMiddleware(secret_key=Secret(SECRET_KEY)),
        # 认证中间件
        Middleware(AuthenticationMiddleware, backend=JWTAuthBackend()),
    ],
    routes=routes,
)

# 测试用例
if __name__ == "__main__":
    from starlette.testclient import TestClient
    client = TestClient(app)
    # 登录测试
    response = client.post("/login", data={"username": "admin", "password": "password123"})
    print(response.json())
