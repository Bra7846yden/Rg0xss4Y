# 代码生成时间: 2025-08-31 09:00:57
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
import uvicorn
from functools import wraps
from typing import Callable

# 模拟数据库存储用户信息和权限
users_db = {
    'admin': {'password': 'adminpass', 'permissions': ['read', 'write', 'delete']},
    'user': {'password': 'userpass', 'permissions': ['read']},
}

# 错误处理装饰器
def error_handling(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(content={'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

# 身份验证装饰器
def require_user(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(request: Request):
        user = request.headers.get('User')
        password = request.headers.get('Password')
        if user and password and users_db.get(user) and users_db[user]['password'] == password:
            return await func(request)
        else:
            return JSONResponse(content={'error': 'Unauthorized'}, status_code=HTTP_401_UNAUTHORIZED)
    return wrapper

# 角色权限装饰器
def require_permission(permission: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request):
            user = request.headers.get('User')
            if user and users_db.get(user) and permission in users_db[user]['permissions']:
                return await func(request)
            else:
                return JSONResponse(content={'error': 'Forbidden'}, status_code=HTTP_403_FORBIDDEN)
        return wrapper
    return decorator

# 用户权限管理系统应用
class UserPermissionManagement(Starlette):
    def __init__(self):
        super().__init__(routes=[
            Route('/users', endpoint=self.list_users, methods=['GET']),
            Route('/users/{username}', endpoint=self.get_user, methods=['GET']),
            Route('/users/{username}/permissions', endpoint=self.update_permissions, methods=['POST']),
        ])

    @error_handling
    @require_user
    async def list_users(self, request: Request):
        return JSONResponse(content={'users': list(users_db.keys())}, status_code=HTTP_200_OK)

    @error_handling
    @require_user
    async def get_user(self, request: Request):
        username = request.path_params['username']
        if username in users_db:
            return JSONResponse(content={'user': users_db[username]}, status_code=HTTP_200_OK)
        else:
            return JSONResponse(content={'error': 'User not found'}, status_code=HTTP_404_NOT_FOUND)

    @error_handling
    @require_user
    @require_permission('write')
    async def update_permissions(self, request: Request):
        username = request.path_params['username']
        permissions = request.json().get('permissions')
        if username in users_db and permissions:
            users_db[username]['permissions'] = permissions
            return JSONResponse(content={'message': 'Permissions updated'}, status_code=HTTP_200_OK)
        else:
            return JSONResponse(content={'error': 'User not found or invalid permissions'}, status_code=HTTP_404_NOT_FOUND)

# 运行服务器
if __name__ == '__main__':
    uvicorn.run(UserPermissionManagement(), host='0.0.0.0', port=8000)