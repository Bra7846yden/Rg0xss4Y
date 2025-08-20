# 代码生成时间: 2025-08-21 02:50:21
# user_auth_service.py

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from starlette.requests import Request
import jwt
import datetime
from typing import Optional

# 用于身份验证的密钥
SECRET_KEY = 'your_secret_key_here'
ALGORITHM = 'HS256'

# 认证相关的配置
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 模拟用户数据库，实际应用中应替换为数据库查询
users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'},
}

def generate_token(user_id: str) -> str:
    """生成JWT令牌"""
    to_encode = {'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 'sub': user_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str) -> Optional[str]:
    """验证用户名和密码，成功返回用户ID，失败返回None"""
    user = users.get(username)
    if user and user['password'] == password:
        return user['username']
    return None

async def login(request: Request) -> JSONResponse:
    """登录接口，验证用户身份并返回JWT令牌"""
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return JSONResponse({'error': 'Username and password are required'}, status_code=HTTP_401_UNAUTHORIZED)
    user_id = await authenticate_user(username, password)
    if not user_id:
        return JSONResponse({'error': 'Invalid credentials'}, status_code=HTTP_401_UNAUTHORIZED)
    token = generate_token(user_id)
    return JSONResponse({'access_token': token, 'token_type': 'bearer'}, status_code=HTTP_200_OK)

async def requires_auth(func):
    """装饰器，用于检查JWT令牌"""
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JSONResponse({'error': 'Authorization token is required'}, status_code=HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return JSONResponse({'error': 'Token has expired'}, status_code=HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return JSONResponse({'error': 'Invalid token'}, status_code=HTTP_401_UNAUTHORIZED)
        return await func(request, *args, **kwargs)
    return wrapper

# 路由配置
routes = [
    Route('/login', login, methods=['POST']),
    Route('/protected', requires_auth(lambda request: JSONResponse({'message': 'You have access to the protected endpoint!'}) ), methods=['GET']),
]

# 创建Starlette应用
app = Starlette(debug=True, routes=routes)
