# 代码生成时间: 2025-08-07 15:53:34
import hashlib
aiohttp
def calculate_hash(data: str) -> str:
    """Calculate the SHA256 hash of the provided data."""
    try:
        return hashlib.sha256(data.encode()).hexdigest()
    except Exception as e:
        raise ValueError(f"Failed to calculate hash: {e}")

def hash_view(request):
    """Endpoint handler for calculating hash."""
    data = request.query.get("data", "")
    try:
# 添加错误处理
        result = calculate_hash(data)
        return {"success": True, "data": data, "hash": result}
    except ValueError as e:
        return {"success": False, "message": str(e)}
async def run_app():
    """Run the Starlette application."""
    app = aiohttp.web.Application()
    async def hash_endpoint(request):
        return aiohttp.web.json_response(hash_view(request))
    app.router.add_get("/hash", hash_endpoint)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, 'localhost', 8000)
    await site.start()
    print("Server started at http://localhost:8000")
# 添加错误处理
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
# 添加错误处理
    finally:
        await runner.cleanup()

def main():
    """Entry point for the application."""
    asyncio.run(run_app())
# TODO: 优化性能
if __name__ == '__main__':
    main()