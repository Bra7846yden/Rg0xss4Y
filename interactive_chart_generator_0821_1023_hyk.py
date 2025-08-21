# 代码生成时间: 2025-08-21 10:23:47
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
import plotly
import plotly.graph_objects as go
def create_chart(data):
    # 创建图表
    chart = go.Figure()
    chart.add_trace(go.Scatter(x=data['x'], y=data['y']))
    chart.update_layout(title_text='Interactive Chart', xaxis_title='X Axis', yaxis_title='Y Axis')
    return chart.to_json()

class ChartGenerator:
    def __init__(self, data):
        self.data = data

    def generate_chart(self):
        try:
            return create_chart(self.data)
        except Exception as e:
            # 如果数据不符合要求，返回错误信息
            return JSONResponse({'error': str(e)})

def chart_route(request):
    # 解析请求数据
    data = request.json()
    if not data or 'x' not in data or 'y' not in data:
        return JSONResponse({'error': 'Invalid data'}, status_code=400)

    # 生成图表
    generator = ChartGenerator(data)
    chart = generator.generate_chart()
    return JSONResponse(chart)

# 定义路由
routes = [
    Route('/chart', chart_route, methods=['POST']),
]

# 创建Starlette应用
app = Starlette(debug=True, routes=routes)
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

"""
Interactive Chart Generator
=========================

A Starlette application that generates interactive charts from user-provided data.

Usage:
    Send a POST request to /chart with JSON data containing 'x' and 'y' arrays.
    The response will be a JSON object representing the chart.

Example Request:
    curl -X POST -H 'Content-Type: application/json' -d '{"x": [1, 2, 3], "y": [4, 5, 6]}' http://localhost:8000/chart

"""