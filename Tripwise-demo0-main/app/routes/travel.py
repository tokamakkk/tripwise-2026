"""
旅行规划路由
Travel Planning Routes

处理旅行规划相关的API端点。
Handles travel planning related API endpoints.

Endpoints:
    POST /api/travel/plan - 创建旅行计划（需认证）
    GET /api/travel/plans - 获取用户的所有旅行计划（需认证）
    GET /api/travel/plans/<plan_id> - 获取特定旅行计划（需认证）
    DELETE /api/travel/plans/<plan_id> - 删除旅行计划（需认证）
"""

from flask import Blueprint, request, jsonify, g
from app.models.travel_plan import TravelPlanRequest, TravelPlan
from app.services.firebase_service import FirebaseService
from app.services.ai_service import AIService
from app.utils.decorators import require_auth, handle_errors
from app.utils.validators import validate_travel_request
from pydantic import ValidationError
from datetime import datetime

travel_bp = Blueprint('travel', __name__)


@travel_bp.route('/plan', methods=['POST'])
@require_auth
@handle_errors
def create_travel_plan():
    """
    创建旅行计划
    Create Travel Plan
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Body:
        {
            "from_location": "北京",
            "destination": "成都",
            "num_people": 2,
            "duration": 5,
            "budget": 5000.0,  (optional)
            "preferences": {...}  (optional)
        }
    
    Returns:
        {
            "message": "Travel plan created successfully",
            "plan_id": "...",
            "status": "processing"
        }
    """
    user_id = g.user_id
    data = request.get_json()
    
    # 验证请求数据
    is_valid, error_msg = validate_travel_request(data)
    if not is_valid:
        return jsonify({
            'error': 'Validation Error',
            'message': error_msg
        }), 400
    
    try:
        # 创建请求对象
        travel_request = TravelPlanRequest(**data)
    except ValidationError as e:
        return jsonify({
            'error': 'Validation Error',
            'details': e.errors()
        }), 400
    
    # 创建初始计划记录
    plan_data = {
        'user_id': user_id,
        'request': travel_request.dict(),
        'status': 'processing',
        'created_at': datetime.utcnow().isoformat(),
        'flights': [],
        'accommodations': [],
        'itinerary': [],
        'total_cost': None,
        'raw_output': None
    }
    
    # 保存到数据库
    plan_id = FirebaseService.save_travel_plan(user_id, plan_data)
    
    # 异步生成旅行计划（这里简化为同步，生产环境应使用异步任务队列）
    try:
        ai_result = AIService.generate_travel_plan(travel_request)
        
        # 更新计划状态
        update_data = {
            'status': 'completed' if ai_result['success'] else 'failed',
            'raw_output': ai_result.get('raw_output'),
            'parsed_result': ai_result.get('parsed_result'),
        }
        
        if not ai_result['success']:
            update_data['error'] = ai_result.get('error')
        
        FirebaseService.update_travel_plan(user_id, plan_id, update_data)
        
    except Exception as e:
        # 如果AI生成失败，更新状态
        FirebaseService.update_travel_plan(user_id, plan_id, {
            'status': 'failed',
            'error': str(e)
        })
    
    return jsonify({
        'message': 'Travel plan created successfully',
        'plan_id': plan_id,
        'status': 'processing',
        'info': 'The AI agents are working on your travel plan. Please check back in a moment.'
    }), 202


@travel_bp.route('/plans', methods=['GET'])
@require_auth
@handle_errors
def get_travel_plans():
    """
    获取用户的所有旅行计划
    Get All Travel Plans for User
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Returns:
        {
            "plans": [
                {
                    "plan_id": "...",
                    "status": "completed",
                    "created_at": "...",
                    "request": {...}
                },
                ...
            ],
            "count": 5
        }
    """
    user_id = g.user_id
    
    # 获取所有计划
    plans = FirebaseService.get_travel_plans(user_id)
    
    return jsonify({
        'plans': plans,
        'count': len(plans)
    }), 200


@travel_bp.route('/plans/<plan_id>', methods=['GET'])
@require_auth
@handle_errors
def get_travel_plan(plan_id):
    """
    获取特定旅行计划
    Get Specific Travel Plan
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Returns:
        {
            "plan": {
                "plan_id": "...",
                "status": "completed",
                "request": {...},
                "flights": [...],
                "accommodations": [...],
                "itinerary": [...],
                "total_cost": 4500.0,
                "raw_output": "...",
                "parsed_result": {...}
            }
        }
    """
    user_id = g.user_id
    
    # 获取计划
    plan = FirebaseService.get_travel_plan(user_id, plan_id)
    
    if not plan:
        return jsonify({
            'error': 'Not Found',
            'message': 'Travel plan not found'
        }), 404
    
    return jsonify({
        'plan': plan
    }), 200


@travel_bp.route('/plans/<plan_id>', methods=['DELETE'])
@require_auth
@handle_errors
def delete_travel_plan(plan_id):
    """
    删除旅行计划
    Delete Travel Plan
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Returns:
        {
            "message": "Travel plan deleted successfully"
        }
    """
    user_id = g.user_id
    
    # 验证计划是否存在
    plan = FirebaseService.get_travel_plan(user_id, plan_id)
    if not plan:
        return jsonify({
            'error': 'Not Found',
            'message': 'Travel plan not found'
        }), 404
    
    # 删除计划
    FirebaseService.delete_travel_plan(user_id, plan_id)
    
    return jsonify({
        'message': 'Travel plan deleted successfully'
    }), 200


@travel_bp.route('/plans/<plan_id>/status', methods=['GET'])
@require_auth
@handle_errors
def get_plan_status(plan_id):
    """
    获取旅行计划状态
    Get Travel Plan Status
    
    用于轮询检查计划生成进度。
    Used for polling to check plan generation progress.
    
    Headers:
        Authorization: Bearer <firebase_id_token>
    
    Returns:
        {
            "plan_id": "...",
            "status": "processing|completed|failed",
            "created_at": "..."
        }
    """
    user_id = g.user_id
    
    # 获取计划
    plan = FirebaseService.get_travel_plan(user_id, plan_id)
    
    if not plan:
        return jsonify({
            'error': 'Not Found',
            'message': 'Travel plan not found'
        }), 404
    
    return jsonify({
        'plan_id': plan_id,
        'status': plan.get('status', 'unknown'),
        'created_at': plan.get('created_at'),
        'error': plan.get('error') if plan.get('status') == 'failed' else None
    }), 200

