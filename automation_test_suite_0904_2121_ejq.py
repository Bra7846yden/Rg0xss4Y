# 代码生成时间: 2025-09-04 21:21:35
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Automation Test Suite using Starlette framework

This script is designed to setup a test suite for APIs built with Starlette.
It demonstrates how to structure a test suite, handle errors, and document code in line
with Python best practices.
"""

import os
import pytest
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.responses import JSONResponse

# Mock API endpoints
async def homepage(request):
    """
    Return a simple welcome message.
    """
    return JSONResponse({'message': 'Welcome to the API!'})

async def echo(request):
    """
    Return the request data.
    """
    return JSONResponse(request.json())

# Setup the test client
def app():
    """
    Create the test Starlette app with the routes.
    """
    routes = [
        ('/', homepage),
        ('/echo', echo)
    ]
    return TestClient(Starlette(routes=routes))

# Test cases
class TestAPIRoutes:
    """
    Test the API routes.
    """
    def test_homepage(self, client):
        """
        Test the homepage returns the correct welcome message.
        """
        response = client.get('/')
        assert response.status_code == 200
        assert response.json() == {'message': 'Welcome to the API!'}

    def test_echo(self, client):
        """
        Test the echo endpoint returns the input data.
        """
        input_data = {'key': 'value'}
        response = client.post('/echo', json=input_data)
        assert response.status_code == 200
        assert response.json() == input_data

# Fixture to setup the TestClient
@pytest.fixture
def client():
    """
    Create a TestClient instance for the Starlette app.
    """
    return app()

# Run pytest to execute the tests
if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__]))