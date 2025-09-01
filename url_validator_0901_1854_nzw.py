# 代码生成时间: 2025-09-01 18:54:27
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from urllib.parse import urlparse
import requests

# 定义一个URL验证函数
def validate_url(url: str) -> bool:
    # 解析URL
    parsed_url = urlparse(url)
    # 检查是否有协议和网络位置
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return False
    try:
        # 发起HEAD请求以检查URL是否可达
        response = requests.head(url)
        # 如果响应状态码为200，则URL有效
        return response.status_code == 200
    except requests.RequestException:
        # 如果请求失败，则URL无效
        return False

# 定义一个星号应用
app = Starlette(debug=True)

# 定义路由和对应的处理函数
@app.route("/validate", methods=["POST"])
async def validate(request):
    # 获取请求体中的URL数据
    data = await request.json()
    url_to_validate = data.get("url")
    if not url_to_validate:
        return JSONResponse({"error": "URL parameter is missing"}, status_code=400)
    
    # 验证URL是否有效
    is_valid = validate_url(url_to_validate)
    if is_valid:
        return JSONResponse({"message": "URL is valid"})
    else:
        return JSONResponse({"message": "URL is invalid"}, status_code=400)

# 将路由添加到应用中
app.add_route("/validate", validate)

# 以下为主函数，用于启动应用
if __name__ == "__main__":
    # 启动星号应用
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)