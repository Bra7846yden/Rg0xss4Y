# 代码生成时间: 2025-09-06 08:51:46
import asyncio
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import uvicorn
import plotly.graph_objects as go
import json

# 定义一个函数来生成一个简单的交互式图表
def generate_chart(data):
    chart = go.Figure(data)
    return chart.to_html(full_html=False)

# 定义一个函数来处理图表数据的请求
async def chart_data(request: Request):
    try:
        # 获取请求中的JSON数据
        data = await request.json()
        # 检查数据是否有效
        if not data or 'type' not in data or 'values' not in data:
            return JSONResponse({'error': 'Invalid data'}, status_code=400)
        # 生成图表并返回HTML响应
        chart_html = generate_chart(data['values'])
        return HTMLResponse(chart_html)
    except json.JSONDecodeError:
        return JSONResponse({'error': 'Invalid JSON'}, status_code=400)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

# 定义Starlette应用程序
app = Starlette(
    debug=True,
    routes=[
        Route('/chart', endpoint=chart_data, methods=['POST'])
    ]
)

# 运行应用程序
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

"""
Interactive Chart Generator

This application uses Starlette framework to create an interactive chart generator.
It accepts POST requests with JSON data containing chart configuration and values.
The chart is then generated and returned as an HTML response.

Usage:
1. Send a POST request to /chart with JSON data in the following format:
   {
       "type": "bar",
       "values": [
           {
               "x": [1, 2, 3],
               "y": [4, 5, 6]
           }
       ]
   }
2. The response will contain the HTML code for the generated chart.
"""