"""
认证路由
Authentication Routes

处理用户认证相关的API端点。
Handles user authentication related API endpoints.

Endpoints:
    POST /api/auth/register - 用户注册
    POST /api/auth/login - 用户登录
    GET /api/auth/profile - 获取用户资料（需认证）
    PUT /api/auth/profile - 更新用户资料（需认证）
"""

from flask import Blueprint, request, jsonify, g
from app.models.user import UserRegister, UserLogin, UserProfile
from app.services.firebase_service import FirebaseService
from app.utils.decorators import require_auth, handle_errors
from app.utils.validators import validate_email
from pydantic import ValidationError
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@handle_errors
def register():
    """
    用户注册
    User Registration
    
    Body:
        {
            "email": "user@example.com",
            "password": "password123",
            "display_name": "John Doe"  (optional)
        }
    
    Returns:
        {
            "message": "User registered successfully",
            "user": {
                "uid": "firebase_uid",
                "email": "user@example.com",
                "display_name": "John Doe"
            }
        }
    """
    data = request.get_json()
    
    # 验证请求数据
    try:
        user_data = UserRegister(**data)
    except ValidationError as e:
        return jsonify({
            'error': 'Validation Error',
            'details': e.errors()
        }), 400
    
    # 创建用户
    try:
        user = FirebaseService.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        
        # 在Realtime Database中保存用户数据
        user_db_data = {
            'email': user['email'],
            'display_name': user['display_name'],
            'created_at': datetime.utcnow().isoformat(),
            'preferences': {}
        }
        FirebaseService.update_user_data(user['uid'], user_db_data)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Registration Failed',
            'message': str(e)
        }), 400


@auth_bp.route('/login', methods=['POST'])
@handle_errors
def login():
    """
    用户登录
    User Login
    
    注意：实际的登录验证通常在客户端通过Firebase SDK完成。
    此端点主要用于验证token和获取用户信息。
    
    Body:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    
    Returns:
        {
            "message": "Login endpoint - use Firebase SDK on client",
            "info": "..."
        }
    """
    # Firebase认证通常在客户端完成
    # 这里返回说明信息
    return jsonify({
        'message': 'Please use Firebase Authentication SDK on client side',
        'info': 'After authentication, include the ID token in Authorization header',
        'example': 'Authorization: Bearer <firebase_id_token>'
    }), 200


@auth_bp.route('/verify', methods=['POST'])
@handle_errors
def verify_token():
    """
    验证Token
    Verify Token
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Returns:
        {
            "valid": true,
            "user": {...}
        }
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({
            'valid': False,
            'error': 'No authorization header'
        }), 401
    
    try:
        token = auth_header.split(' ')[1]
        decoded_token = FirebaseService.verify_token(token)
        
        # 获取用户信息
        user = FirebaseService.get_user(decoded_token['uid'])
        
        # 更新最后登录时间
        FirebaseService.update_user_data(
            decoded_token['uid'],
            {'last_login': datetime.utcnow().isoformat()}
        )
        
        return jsonify({
            'valid': True,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 401


@auth_bp.route('/profile', methods=['GET'])
@require_auth
@handle_errors
def get_profile():
    """
    获取用户资料
    Get User Profile
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Returns:
        {
            "user": {
                "uid": "...",
                "email": "...",
                "display_name": "...",
                "preferences": {...}
            }
        }
    """
    user_id = g.user_id
    
    # 从Firebase Auth获取用户信息
    user = FirebaseService.get_user(user_id)
    
    # 从Realtime Database获取额外数据
    user_data = FirebaseService.get_user_data(user_id)
    
    if user_data:
        user.update(user_data)
    
    return jsonify({
        'user': user
    }), 200


@auth_bp.route('/profile', methods=['PUT'])
@require_auth
@handle_errors
def update_profile():
    """
    更新用户资料
    Update User Profile
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Body:
        {
            "display_name": "New Name",
            "preferences": {
                "currency": "CNY",
                "language": "zh-CN"
            }
        }
    
    Returns:
        {
            "message": "Profile updated successfully",
            "user": {...}
        }
    """
    user_id = g.user_id
    data = request.get_json()
    
    # 验证数据
    try:
        profile_data = UserProfile(**data)
    except ValidationError as e:
        return jsonify({
            'error': 'Validation Error',
            'details': e.errors()
        }), 400
    
    # 准备更新数据
    update_data = {}
    if profile_data.display_name is not None:
        update_data['display_name'] = profile_data.display_name
    if profile_data.preferences is not None:
        update_data['preferences'] = profile_data.preferences
    
    # 更新数据库
    updated_user = FirebaseService.update_user_data(user_id, update_data)
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': updated_user
    }), 200

