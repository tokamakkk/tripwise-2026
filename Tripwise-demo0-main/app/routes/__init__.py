"""
API路由模块
API Routes Module

定义所有API端点。
Defines all API endpoints.
"""

from app.routes.auth import auth_bp
from app.routes.travel import travel_bp

__all__ = ['auth_bp', 'travel_bp']

