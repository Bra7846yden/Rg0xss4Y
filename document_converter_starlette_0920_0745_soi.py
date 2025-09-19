# 代码生成时间: 2025-09-20 07:45:16
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
# 改进用户体验
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
# TODO: 优化性能
import json
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

# Define constants for supported file formats
SUPPORTED_FORMATS = {"docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "pdf": "application/pdf"}

# Define the DocumentConverter class
# 增强安全性
class DocumentConverter:
    def __init__(self):
        self.doc = None

    def load_document(self, file_path):
# 改进用户体验
        if not os.path.exists(file_path):
            raise FileNotFoundError("The document file was not found.")
        try:
            self.doc = Document(file_path)
        except Exception as e:
            raise ValueError("Failed to load the document: " + str(e))

    def convert_to_json(self):
        if self.doc is None:
            raise ValueError("No document loaded.")
        content = []
        for para in self.doc.paragraphs:
            content.append({
# 增强安全性
                "text": para.text,
                "alignment": para.alignment.value,
                "font_size": para.runs[0].font.size
            })
# NOTE: 重要实现细节
        return json.dumps(content, ensure_ascii=False)
# 优化算法效率

# Define the Starlette application
app = Starlette(routes=[
# 改进用户体验
    Route("/convert", endpoint=convert_endpoint, methods=["POST"]),
])

async def convert_endpoint(request):
    # Get the uploaded file
    file = await request.form()
    if "document" not in file.files:
        return JSONResponse(
            content={"error": "No document provided"},
# 增强安全性
            status_code=HTTP_400_BAD_REQUEST
        )

    # Check if the file is in a supported format
# FIXME: 处理边界情况
    file_item = file.files["document"]
    file_type = file_item.content_type
    if file_type not in SUPPORTED_FORMATS.values():
        return JSONResponse(
# 改进用户体验
            content={"error": "Unsupported file format"},
            status_code=HTTP_400_BAD_REQUEST
        )
# 改进用户体验

    # Temporarily save the file to the server
    file_path = f"/tmp/{file_item.filename}"
    with open(file_path, "wb") as f:
        f.write(await file_item.read())

    try:
        converter = DocumentConverter()
        converter.load_document(file_path)
        json_content = converter.convert_to_json()
    except (FileNotFoundError, ValueError) as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=HTTP_400_BAD_REQUEST
        )
    finally:
# 改进用户体验
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

    # Return the converted content as a JSON response
    return JSONResponse(content=json_content)

# Documentation for the /convert endpoint
@app.route("/docs")
async def api_documentation(request):
    return JSONResponse(content={
        "description": "Converts a document to JSON format",
        "endpoint": "/convert",
        "methods": ["POST"],
        "request": {
            "document": "File to be converted (supported formats: DOCX)"
        },
# 增强安全性
        "response": {
# 添加错误处理
            "type": "JSON",
            "content": "Converted document content"
        },
        "errors": {
            "400": "Bad Request (e.g., no document provided, unsupported format)",
            "404": "Not Found"
        }
    })
# 增强安全性
