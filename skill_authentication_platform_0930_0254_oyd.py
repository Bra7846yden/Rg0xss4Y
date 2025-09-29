# 代码生成时间: 2025-09-30 02:54:27
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

import uvicorn
from typing import List, Dict

# 模拟数据库存储技能信息
skills_db: Dict[str, Dict[str, str]] = {
    "skill1": {"name": "Python", "description": "Programming language"},
    "skill2": {"name": "JavaScript", "description": "Programming language"},
}

# 获取技能列表的路由
@Route("/skills", methods=["GET"])
def list_skills(request):
    try:
        return JSONResponse(skills_db, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 获取单个技能的路由
@Route("/skills/{skill_id}", methods=["GET"])
def get_skill(request, skill_id: str):
    try:
        skill = skills_db.get(skill_id)
        if skill is None:
            return JSONResponse({"error": "Skill not found"}, status_code=HTTP_404_NOT_FOUND)
        return JSONResponse(skill, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 添加技能的路由
@Route("/skills", methods=["POST"])
def add_skill(request):
    data = request.json()
    try:
        if not data.get("name"):
            return JSONResponse({"error": "Skill name is required"}, status_code=HTTP_400_BAD_REQUEST)
        skill_id = len(skills_db) + 1  # 简单的ID生成
        skills_db[str(skill_id)] = data
        return JSONResponse(skills_db[str(skill_id)], status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 更新技能的路由
@Route("/skills/{skill_id}", methods=["PUT"])
def update_skill(request, skill_id: str):
    data = request.json()
    try:
        if skill_id not in skills_db:
            return JSONResponse({"error": "Skill not found"}, status_code=HTTP_404_NOT_FOUND)
        skills_db[skill_id].update(data)
        return JSONResponse(skills_db[skill_id], status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 删除技能的路由
@Route("/skills/{skill_id}", methods=["DELETE"])
def delete_skill(request, skill_id: str):
    try:
        if skill_id not in skills_db:
            return JSONResponse({"error": "Skill not found"}, status_code=HTTP_404_NOT_FOUND)
        del skills_db[skill_id]
        return JSONResponse({"message": "Skill deleted"}, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 创建Starlette应用并注册路由
app = Starlette(routes=[
    Route("/skills", list_skills),
    Route("/skills/{skill_id}", get_skill),
    Route("/skills", add_skill, methods=["POST"]),
    Route("/skills/{skill_id}", update_skill, methods=["PUT"]),
    Route("/skills/{skill_id}", delete_skill, methods=["DELETE"]),
])

# 运行Uvicorn服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)