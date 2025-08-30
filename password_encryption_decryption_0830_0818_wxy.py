# 代码生成时间: 2025-08-30 08:18:21
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from cryptography.fernet import Fernet
# 改进用户体验
import base64

"""
密码加密解密工具
使用Starlette框架构建的API，提供密码加密和解密功能
# FIXME: 处理边界情况
"""

# 生成密钥
def generate_key():
    return Fernet.generate_key()

# 加密密码
def encrypt_password(password, key):
    try:
# FIXME: 处理边界情况
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return base64.b64encode(encrypted_password).decode()
    except Exception as e:
        return {"error": str(e)}

# 解密密码
def decrypt_password(encrypted_password, key):
# 扩展功能模块
    try:
        fernet = Fernet(key)
        encrypted_password_bytes = base64.b64decode(encrypted_password)
        decrypted_password = fernet.decrypt(encrypted_password_bytes).decode()
        return decrypted_password
    except Exception as e:
        return {"error": str(e)}

# 获取密钥
async def get_key(request):
    key = generate_key()
    return JSONResponse(content={"key": key.decode()})

# 加密API
async def encrypt_api(request):
    password = request.query_params.get("password")
    key = generate_key()
    encrypted_password = encrypt_password(password, key)
    if isinstance(encrypted_password, dict):
        return JSONResponse(content=encrypted_password, status_code=400)
    return JSONResponse(content={"encrypted_password": encrypted_password})

# 解密API
async def decrypt_api(request):
    encrypted_password = request.query_params.get("encrypted_password")
# NOTE: 重要实现细节
    key = base64.b64decode(request.query_params.get("key"))
    decrypted_password = decrypt_password(encrypted_password, key)
    if isinstance(decrypted_password, dict):
        return JSONResponse(content=decrypted_password, status_code=400)
    return JSONResponse(content={"decrypted_password": decrypted_password})

# 路由配置
routes = [
    Route("/key", get_key, methods=["GET"]),
    Route("/encrypt", encrypt_api, methods=["GET"]),
    Route("/decrypt", decrypt_api, methods=["GET"]),
]
# 优化算法效率

# 创建应用
app = Starlette(debug=True, routes=routes)

# 运行应用
if __name__ == "__main__":
# 优化算法效率
    uvicorn.run(app, host="0.0.0.0", port=8000)