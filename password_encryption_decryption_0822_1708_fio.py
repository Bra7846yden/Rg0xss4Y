# 代码生成时间: 2025-08-22 17:08:22
# password_encryption_decryption.py
# This module provides a simple password encryption and decryption tool using the Starlette framework.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import base64
import bcrypt

# Function to generate a password hash
def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    
    Args:
        password (str): The password to be hashed.
    
    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify a password against a hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a bcrypt hash.
    
    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The bcrypt hash to verify against.
    
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Route for encrypting a password
async def encrypt_password(request):
    """
    Encrypts a password and returns the hash.
    
    Args:
        request (Request): The Starlette request object.
    
    Returns:
        JSONResponse: A JSON response with the hashed password.
    """
    try:
        password = await request.json()
        hashed = hash_password(password['password'])
        return JSONResponse({'hashed_password': hashed.decode('utf-8')}, status_code=HTTP_200_OK)
    except KeyError:
        return JSONResponse({'error': 'Password field is missing'}, status_code=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Route for decrypting a password (verification)
async def decrypt_password(request):
    """
    Decrypts a password by verifying it against a hash.
    
    Args:
        request (Request): The Starlette request object.
    
    Returns:
        JSONResponse: A JSON response indicating if the password matches the hash.
    """
    try:
        data = await request.json()
        is_correct = verify_password(data['password'], data['hashed_password'])
        return JSONResponse({'is_correct': is_correct}, status_code=HTTP_200_OK)
    except KeyError:
        return JSONResponse({'error': 'Password or hashed_password field is missing'}, status_code=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Create a Starlette application with routes
app = Starlette(debug=True, routes=[
    Route('encrypt', encrypt_password, methods=['POST']),
    Route('decrypt', decrypt_password, methods=['POST'])
])

# If running this script directly, run the application
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)