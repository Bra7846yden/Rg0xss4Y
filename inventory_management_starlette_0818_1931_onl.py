# 代码生成时间: 2025-08-18 19:31:14
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from uuid import uuid4
import logging

# 定义一个简单的库存管理系统
class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item_id, item_name, quantity):
        """
        添加或更新库存项
        :param item_id: 唯一标识符
        :param item_name: 物品名称
        :param quantity: 库存数量
        """
        if not item_name or quantity <= 0:
            raise ValueError("Item name and quantity must be provided and quantity must be positive.")
        self.inventory[item_id] = {'name': item_name, 'quantity': quantity}

    def get_item(self, item_id):
        """
        根据ID获取库存项
        :param item_id: 唯一标识符
        :return: 库存项信息
        """
        return self.inventory.get(item_id, None)

    def remove_item(self, item_id):
        """
        从库存中删除项目
        :param item_id: 唯一标识符
        """
        if item_id in self.inventory:
            del self.inventory[item_id]


# 创建库存管理类的实例
inventory_manager = InventoryManager()

# 路由和视图函数
routes = [
    Route("/items/", endpoint=addItem, methods=["POST"]),
    Route("/items/{item_id}", endpoint=getItem, methods=["GET"]),
    Route("/items/{item_id}", endpoint=removeItem, methods=["DELETE"]),
]

# 添加库存项的视图函数
async def addItem(request):
    try:
        data = await request.json()
        item_id = str(uuid4())
        item_name = data.get("name")
        quantity = data.get("quantity")
        inventory_manager.add_item(item_id, item_name, quantity)
        return JSONResponse(content={"item_id": item_id, "message": "Item added successfully"}, status_code=HTTP_201_CREATED)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return JSONResponse(content={"error": "Invalid JSON data"}, status_code=HTTP_400_BAD_REQUEST)

# 获取库存项的视图函数
async def getItem(request):
    item_id = request.path_params.get("item_id")
    item = inventory_manager.get_item(item_id)
    if item:
        return JSONResponse(content=item, status_code=HTTP_200_OK)
    else:
        return JSONResponse(content={"error": "Item not found"}, status_code=HTTP_404_NOT_FOUND)

# 移除库存项的视图函数
async def removeItem(request):
    item_id = request.path_params.get("item_id")
    inventory_manager.remove_item(item_id)
    return JSONResponse(content={"message": "Item removed successfully"}, status_code=HTTP_200_OK)

# 创建Starlette应用并添加路由
app = Starlette(routes=routes, debug=True)

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)