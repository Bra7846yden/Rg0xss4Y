# 代码生成时间: 2025-09-15 06:42:00
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
import functools
from cachetools import TTLCache, cached
from typing import Any, Callable


# Define a decorator for cache
def cache_with_key(key: str, ttl: int = 300):
    cache = TTLCache(maxsize=100, ttl=ttl)  # Initialize cache with TTL and max size
    cache_misses = cache.misses
    cache_hits = cache.hits

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal cache_misses, cache_hits
            cache_key = key.format(*args, **kwargs)
            if cache_key in cache:
                cache_hits += 1
                return cache[cache_key]
            else:
                cache_misses += 1
                result = await func(*args, **kwargs)
                cache[cache_key] = result
                return result
        return wrapper
    return decorator


# Example cacheable function
@cache_with_key(key="{user_id}", ttl=300)
async def get_user_data(user_id: int) -> dict:
    # Simulate a database request
    await asyncio.sleep(1)  # Simulate network or I/O delay
    return {"id": user_id, "name": "John Doe"}


# Create a Starlette app
app = Starlette(debug=True)

# Define route to use the cached function
@app.route("/user/{user_id}", methods=["GET"])
async def user_route(request):
    try:
        user_id = int(request.path_params["user_id"])
        user_data = await get_user_data(user_id)
        return JSONResponse(status_code=HTTP_200_OK, content=user_data)
    except ValueError:
        # Handle the case where user_id is not an integer
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"error": "Invalid user ID"})
    except Exception as e:
        # Handle any other exceptions that may occur
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})

# Define a route to display cache statistics
@app.route("/cache-stats", methods=["GET"])
async def cache_stats_route(request):
    return JSONResponse(
        status_code=HTTP_200_OK,
        content={
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
        },
    )

# Run the Starlette app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cache_service:app", host="127.0.0.1", port=8000)