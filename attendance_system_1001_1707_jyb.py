# 代码生成时间: 2025-10-01 17:07:53
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
from typing import Dict

"""
考勤打卡系统
"""

# 假设存储考勤数据的字典
attendance_records = {}


class AttendanceSystem:
    def __init__(self):
        pass

    def register_employee(self, employee_id: str):
        """
        注册员工
        :param employee_id: 员工ID
        """
        if employee_id in attendance_records:
            return False
        attendance_records[employee_id] = []
        return True

    def clock_in(self, employee_id: str):
        """
        员工打卡
        :param employee_id: 员工ID
        """
        if employee_id not in attendance_records:
            return False
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_records[employee_id].append(now)
        return True

    def get_attendance(self, employee_id: str):
        """
        获取员工考勤记录
        :param employee_id: 员工ID
        """
        if employee_id not in attendance_records:
            return []
        return attendance_records[employee_id]

# 定义API路由
routes = [
    Route("/clock-in/{employee_id}", endpoint=ClockInEndpoint, methods=["POST"]),
    Route("/attendance/{employee_id}", endpoint=AttendanceEndpoint, methods=["GET"]),
]

# 打卡接口
class ClockInEndpoint:
    def __init__(self):
        self.attendance_system = AttendanceSystem()

    async def __call__(self, request):
        try:
            employee_id = request.path_params['employee_id']
            success = self.attendance_system.clock_in(employee_id)
            if success:
                return JSONResponse(
                    status_code=HTTP_200_OK, content={"message": "Clock in successful"}
                )
            else:
                return JSONResponse(
                    status_code=HTTP_400_BAD_REQUEST, content={"message": "Employee not registered"}
                )
        except Exception as e:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST, content={"message": str(e)}
            )

# 获取考勤记录接口
class AttendanceEndpoint:
    def __init__(self):
        self.attendance_system = AttendanceSystem()

    async def __call__(self, request):
        try:
            employee_id = request.path_params['employee_id']
            attendance = self.attendance_system.get_attendance(employee_id)
            return JSONResponse(
                status_code=HTTP_200_OK, content={"attendance": attendance}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTP_400_BAD_REQUEST, content={"message": str(e)}
            )

# 创建Starlette应用
app = Starlette(routes=routes)
