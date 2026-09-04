"""
装饰器模块
Decorators Module

提供API路由的装饰器，如认证、错误处理等。
Provides decorators for API routes such as authentication and error handling.

Decorators:
    - require_auth: 要求Firebase认证
    - handle_errors: 统一错误处理
"""

from functools import wraps
from flask import request, jsonify
from app.services.firebase_service import FirebaseService


def require_auth(f):
    """
    Firebase认证装饰器
    Firebase Authentication Decorator
    
    验证请求头中的Firebase ID token。
    Validates Firebase ID token from request headers.
    
    Usage:
        @require_auth
        def protected_route():
            # user_id available via g.user_id
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取token
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'No authorization header provided'
            }), 401
        
        # 期望格式: "Bearer <token>"
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid authorization header format'
            }), 401
        
        # 验证token
        try:
            decoded_token = FirebaseService.verify_token(token)
            # 将用户信息附加到请求中
            from flask import g
            g.user_id = decoded_token['uid']
            g.user_email = decoded_token.get('email')
        except ValueError as e:
            return jsonify({
                'error': 'Unauthorized',
                'message': str(e)
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def handle_errors(f):
    """
    错误处理装饰器
    Error Handling Decorator
    
    捕获并统一处理函数中的异常。
    Catches and uniformly handles exceptions in functions.
    
    Usage:
        @handle_errors
        def my_route():
            # Your code here
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({
                'error': 'Bad Request',
                'message': str(e)
            }), 400
        except PermissionError as e:
            return jsonify({
                'error': 'Forbidden',
                'message': str(e)
            }), 403
        except Exception as e:
            # 记录错误日志
            print(f"❌ Error in {f.__name__}: {e}")
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500
    
    return decorated_function

