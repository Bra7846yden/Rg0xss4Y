# 代码生成时间: 2025-09-11 11:27:07
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST
import random

# 排序算法实现
def bubble_sort(arr):
    """
    冒泡排序算法实现。
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 应用路由和错误处理
def sort_items(request):
    """
    处理排序请求。
    """
    data = request.json()
    if not data or 'items' not in data:
        return JSONResponse(
            content="{'error': 'Missing items in request'}",
            status_code=HTTP_400_BAD_REQUEST
        )

    arr = data['items']
    sorted_arr = bubble_sort(arr)
    return JSONResponse(content={'items': sorted_arr})

# 创建Starlette应用
app = Starlette(debug=True, routes=[
    Route("/sort", sort_items, methods=['POST']),
])

if __name__ == '__main__':
    # 启动应用
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)