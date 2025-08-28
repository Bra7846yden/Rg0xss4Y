# 代码生成时间: 2025-08-29 04:54:00
import starlette.responses
import starlette.status
from starlette.requests import Request
from typing import List, Tuple


# 定义排序算法服务类
class SortingService:
    # 冒泡排序算法
    @staticmethod
    def bubble_sort(arr: List[int]) -> List[int]:
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    # 插入排序算法
    @staticmethod
    def insertion_sort(arr: List[int]) -> List[int]:
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >=0 and key < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    # 快速排序算法
    @staticmethod
    def quick_sort(arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            less = [x for x in arr[1:] if x <= pivot]
            greater = [x for x in arr[1:] if x > pivot]
            return SortingService.quick_sort(less) + [pivot] + SortingService.quick_sort(greater)


# Starlette路由和端点
async def sort_endpoint(request: Request) -> starlette.responses.JSONResponse:
    # 从请求中获取排序数组和选择的排序算法
    query_params = request.query_params
    unsorted_list = query_params.get('list', type=list)
    sort_algorithm = query_params.get('algorithm', type=str)

    # 检查输入参数的有效性
    if not unsorted_list or not isinstance(unsorted_list, list) or not all(isinstance(x, int) for x in unsorted_list):
        return JSONResponse({'error': 'Invalid list parameter'}, status_code=starlette.status.HTTP_400_BAD_REQUEST)
    if sort_algorithm not in ['bubble', 'insertion', 'quick']:
        return JSONResponse({'error': 'Invalid algorithm parameter'}, status_code=starlette.status.HTTP_400_BAD_REQUEST)

    # 根据选择的算法排序数组
    sorting_service = SortingService()
    if sort_algorithm == 'bubble':
        sorted_list = sorting_service.bubble_sort(unsorted_list)
    elif sort_algorithm == 'insertion':
        sorted_list = sorting_service.insertion_sort(unsorted_list)
    else:  # quick
        sorted_list = sorting_service.quick_sort(unsorted_list)

    # 返回排序后的数组
    return JSONResponse({'sorted_list': sorted_list})

# 定义路由
routes = [
    {'path': '/sort', 'method': 'GET', 'endpoint': sort_endpoint}
]


"""
排序服务模块。
包含三种排序算法：冒泡排序、插入排序和快速排序。
通过Starlette框架提供的HTTP GET请求接收一个未排序的列表和选择的排序算法。
返回排序后的列表。
"""