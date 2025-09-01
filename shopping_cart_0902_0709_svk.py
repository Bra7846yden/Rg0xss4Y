# 代码生成时间: 2025-09-02 07:09:01
# shopping_cart.py

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

# 购物车类
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, quantity):
        """向购物车中添加项目。"""
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id):
        """从购物车中移除项目。"""
        if item_id in self.items:
            del self.items[item_id]
        else:
            return None

    def get_cart(self):
        """返回购物车中的所有项目。"""
        return self.items

    def clear_cart(self):
        """清空购物车。"""
        self.items.clear()

# 星标应用程序
app = Starlette(debug=True)

# 购物车实例
cart = ShoppingCart()

# 路由
routes = [
    Route("/cart", endpoint=cart_endpoint, methods=["GET", "POST"]),
    Route("/cart/{item_id}", endpoint=item_endpoint, methods=["DELETE"]),
]

# 购物车端点
async def cart_endpoint(request):
    if request.method == "GET":
        return JSONResponse(cart.get_cart(), status_code=HTTP_200_OK)
    elif request.method == "POST":
        data = await request.json()
        item_id = data.get("item_id")
        quantity = data.get("quantity")
        if not item_id or not quantity or not isinstance(quantity, int) or quantity < 1:
            return JSONResponse({"error": "Invalid data"}, status_code=HTTP_400_BAD_REQUEST)
        cart.add_item(item_id, quantity)
        return JSONResponse(cart.get_cart(), status_code=HTTP_200_OK)
    else:
        return JSONResponse({"error": "Method not allowed"}, status_code=405)

# 单个项目端点
async def item_endpoint(request, item_id):
    try:
        cart.remove_item(item_id)
        return JSONResponse(cart.get_cart(), status_code=HTTP_200_OK)
    except KeyError:
        return JSONResponse({"error": "Item not found"}, status_code=HTTP_404_NOT_FOUND)

# 添加路由到星标应用程序
for route in routes:
    app.add_route(route)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)