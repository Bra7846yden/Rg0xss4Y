# 代码生成时间: 2025-09-07 22:12:23
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# 模拟数据库
inventory_db = {
    "1": {"name": "Apple", "quantity": 50},
    "2": {"name": "Banana", "quantity": 30},
    "3": {"name": "Cherry", "quantity": 20},
}

# 库存管理系统应用
class InventoryManagement(Starlette):
    def __init__(self):
        super().__init__(routes=get_routes())

# 获取库存条目的路由
def get_routes():
    return [
        Route("/items/", InventoryItems, methods=["GET", "POST"]),
        Route("/items/{item_id}", InventoryItem, methods=["GET", "PUT", "DELETE\]),
    ]

# 库存条目集合处理类
class InventoryItems:
    async def get(self) -> JSONResponse:
        """获取所有库存条目"""
        try:
            return JSONResponse(status_code=HTTP_200_OK, content={"items": list(inventory_db.values())})
        except Exception as e:
            return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

    async def post(self, request) -> JSONResponse:
        """添加新的库存条目"""
        try:
            data = await request.json()
            item_id = str(len(inventory_db) + 1)
            inventory_db[item_id] = data
            return JSONResponse(status_code=HTTP_201_CREATED, content={"item_id": item_id, "item": data})
        except Exception as e:
            return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

# 单个库存条目处理类
class InventoryItem:
    async def get(self, item_id) -> JSONResponse:
        """根据ID获取库存条目"""
        try:
            item = inventory_db.get(item_id)
            if item is None:
                return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"error": "Item not found"})
            return JSONResponse(status_code=HTTP_200_OK, content={"item": item})
        except Exception as e:
            return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

    async def put(self, item_id, request) -> JSONResponse:
        """更新库存条目"""
        try:
            data = await request.json()
            if item_id not in inventory_db:
                return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"error": "Item not found"})
            inventory_db[item_id].update(data)
            return JSONResponse(status_code=HTTP_200_OK, content={"item": inventory_db[item_id]})
        except Exception as e:
            return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

    async def delete(self, item_id) -> JSONResponse:
        """删除库存条目"""
        try:
            if item_id not in inventory_db:
                return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"error": "Item not found"})
            del inventory_db[item_id]
            return JSONResponse(status_code=HTTP_200_OK, content={"message": "Item deleted"})
        except Exception as e:
            return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

# 运行应用
if __name__ == "__main__":
    app = InventoryManagement()
    uvicorn.run(app, host="0.0.0.0", port=8000)