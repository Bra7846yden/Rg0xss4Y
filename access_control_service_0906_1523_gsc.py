# 代码生成时间: 2025-09-06 15:23:17
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import datetime

# Configuration
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Error handler for unauthorized access
async def unauthorized_handler(request, exc):
    return JSONResponse({'detail': 'Unauthorized'}, status_code=HTTP_401_UNAUTHORIZED)


# Error handler for forbidden access
async def forbidden_handler(request, exc):
    return JSONResponse({'detail': 'Forbidden'}, status_code=HTTP_403_FORBIDDEN)


# Middleware to check for JWT tokens and validate them
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Check if the route requires authentication
        if 'auth' in request.scope['path']:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing 'Authorization' header")

            # Verify the JWT token
            try:
                token = auth_header.split()[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            except (jwt.PyJWTError, IndexError):
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

            # Check if the token has expired
            if get_current_time() > payload['exp']:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token has expired")

            # Add the user_id to the request for later use
            request.state.user_id = payload['sub']
        response = await call_next(request)
        return response


# Helper function to get the current time
def get_current_time():
    return datetime.datetime.utcnow()


# Helper function to create a new access token
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = get_current_time() + expires_delta
    else:
        expire = get_current_time() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Route to test authentication
async def auth_test(request):
    # Simulate a protected route
    user_id = request.state.user_id
    return JSONResponse({'message': f'Hello, user {user_id}!'})


# Route to get a new access token
async def get_token(request):
    # Simulate a login endpoint
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    # In a real application, you would verify the credentials against a database
    if username != 'admin' or password != 'admin':
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    user_id = 1  # Simulate a user_id
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    return JSONResponse({'access_token': access_token, 'token_type': 'bearer'})


# Create the Starlette application with the routes
app = Starlette(
    routes=[
        Route('/token', endpoint=get_token, methods=['GET']),
        Route('/auth/test', endpoint=auth_test, methods=['GET'], auth=True),
    ],
    middleware=[
        ('/auth/', AuthMiddleware()),
    ],
    exception_handlers={
        HTTP_401_UNAUTHORIZED: unauthorized_handler,
        HTTP_403_FORBIDDEN: forbidden_handler,
    },
)

# Run the application with uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)