# 代码生成时间: 2025-08-11 05:32:41
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import BaseModel, ValidationError
import logging

# Define a Pydantic model for the order schema
class Order(BaseModel):
    product_id: int
    quantity: int
    customer_id: int

# Define a mock database for demonstration purposes
mock_db = {
    1: {'product_name': 'Laptop', 'stock': 10},
    2: {'product_name': 'Smartphone', 'stock': 5}
}

# Function to check order details and return a response
def process_order(order: Order):
    """
    Processes an order by checking stock and creating an order record.
    """
    product = mock_db.get(order.product_id)
    if not product:
        return JSONResponse(
            content="Product not found",
            status_code=HTTP_400_BAD_REQUEST
        )
    if product['stock'] < order.quantity:
        return JSONResponse(
            content="Insufficient stock",
            status_code=HTTP_400_BAD_REQUEST
        )
    # Update stock in the mock database
    mock_db[order.product_id]['stock'] -= order.quantity
    # Create an order record (this would be replaced with a database operation in a real scenario)
    order_record = {
        'order_id': 1,  # This should be a unique identifier in a real scenario
        'product_name': product['product_name'],
        'quantity': order.quantity,
        'customer_id': order.customer_id
    }
    return JSONResponse(content=order_record, status_code=200)

# Route to handle POST requests for creating an order
async def create_order(request):
    try:
        # Parse the request body and validate it
        order_data = await request.json()
        order = Order(**order_data)
        # Process the order
        return await process_order(order)
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return JSONResponse(
            content=f"Validation error: {e}",
            status_code=HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return JSONResponse(
            content="An unexpected error occurred",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

# Define the routes for the Starlette application
routes = [
    Route("/order", create_order, methods=["POST"]),
]

# Create a Starlette application instance with the defined routes
app = Starlette(routes=routes)

if __name__ == '__main__':
    # Run the application
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
