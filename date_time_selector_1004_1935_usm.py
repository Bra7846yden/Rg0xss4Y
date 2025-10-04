# 代码生成时间: 2025-10-04 19:35:40
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from datetime import datetime
import pytz
from pytz import timezone
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

# 定义一个函数，返回日历页面
async def get_calendar(request):
    return HTMLResponse(
        '<html><body><h1>Date Time Selector</h1>'
        '<form method="post" action="/select_date">'
        '<input type="date" name="date" required><br>'
        '<input type="time" name="time" required><br>'
        '<input type="submit" value="Submit" />'
        '</form></body></html>'
    )

# 定义一个函数，处理日期时间选择
async def select_date(request):
    try:
        # 获取表单提交的日期和时间
        date_str = request.form['date']
        time_str = request.form['time']

        # 解析日期和时间字符串
        date = parse(f'{date_str} {time_str}')

        # 将日期时间转换为UTC并返回
        utc_date = date.astimezone(pytz.utc)
        return JSONResponse(content={'date': utc_date.isoformat()}, status_code=200)
    except Exception as e:
        # 错误处理
        return JSONResponse(content={'error': str(e)}, status_code=400)

# 创建路由
routes = [
    Route('/', get_calendar),
    Route('/select_date', select_date, methods=['POST']),
]

# 创建Starlette应用
app = Starlette(debug=True, routes=routes)

# 测试代码
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)
