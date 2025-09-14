# 代码生成时间: 2025-09-14 17:53:29
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from starlette.requests import Request
from typing import Dict, List, Optional


# ShoppingCartService 负责处理购物车相关逻辑
class ShoppingCartService:
    def __init__(self):
        self.cart = {}

    def add_item(self, user_id: str, item_id: str, quantity: int) -> Dict:
        """
        向用户购物车添加商品
        :param user_id: 用户ID
        :param item_id: 商品ID
        :param quantity: 添加数量
        :return: 更新后的购物车
        """
        if user_id not in self.cart:
            self.cart[user_id] = {}

        self.cart[user_id][item_id] = self.cart.get(user_id, {}).get(item_id, 0) + quantity

        return self.cart[user_id]

    def remove_item(self, user_id: str, item_id: str) -> Dict:
        """
        从用户购物车移除商品
        :param user_id: 用户ID
        :param item_id: 商品ID
        :return: 更新后的购物车
        """
        if user_id in self.cart and item_id in self.cart[user_id]:
            del self.cart[user_id][item_id]
            if not self.cart[user_id]:
                del self.cart[user_id]

        return self.cart.get(user_id, {})

    def get_cart(self, user_id: str) -> Dict:
        """
        获取用户购物车
        :param user_id: 用户ID
        :return: 用户购物车
        """
        return self.cart.get(user_id, {})


# ShoppingCartAPI 负责处理HTTP请求
class ShoppingCartAPI:
    def __init__(self, service: ShoppingCartService):
        self.service = service

    async def add_item_to_cart(self, request: Request) -> JSONResponse:
        """
        处理添加商品到购物车的请求
        """
        data = await request.json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        quantity = data.get('quantity', 1)

        if not user_id or not item_id or not isinstance(quantity, int):
            return JSONResponse(
                content={'error': 'Invalid data'}, status_code=HTTP_400_BAD_REQUEST
            )

        cart = self.service.add_item(user_id, item_id, quantity)
        return JSONResponse(content={'cart': cart}, status_code=HTTP_200_OK)

    async def remove_item_from_cart(self, request: Request) -> JSONResponse:
        """
        处理从购物车移除商品的请求
        """
        data = await request.json()
        user_id = data.get('user_id')
        item_id = data.get('item_id')

        if not user_id or not item_id:
            return JSONResponse(
                content={'error': 'Invalid data'}, status_code=HTTP_400_BAD_REQUEST
            )

        cart = self.service.remove_item(user_id, item_id)
        return JSONResponse(content={'cart': cart}, status_code=HTTP_200_OK)

    async def get_cart(self, request: Request) -> JSONResponse:
        """
        处理获取购物车的请求
        """
        user_id = request.path_params.get('user_id')

        if not user_id:
            return JSONResponse(
                content={'error': 'User ID is required'}, status_code=HTTP_400_BAD_REQUEST
            )

        cart = self.service.get_cart(user_id)
        return JSONResponse(content={'cart': cart}, status_code=HTTP_200_OK)

# 创建Starlette应用
app = Starlette(
    routes=[
        Route('/cart/add', endpoint=ShoppingCartAPI(ShoppingCartService()).add_item_to_cart, methods=['POST']),
        Route('/cart/remove', endpoint=ShoppingCartAPI(ShoppingCartService()).remove_item_from_cart, methods=['POST']),
        Route('/cart/{user_id}', endpoint=ShoppingCartAPI(ShoppingCartService()).get_cart, methods=['GET'])
    ]
)

# 如果直接运行此文件，则启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)