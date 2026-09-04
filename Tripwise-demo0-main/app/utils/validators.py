"""
验证器模块
Validators Module

提供数据验证功能。
Provides data validation functionality.

Functions:
    - validate_travel_request(data): 验证旅行请求数据
    - validate_date_range(start_date, end_date): 验证日期范围
"""

from typing import Dict, Tuple
from datetime import datetime
from app.config import Config


def validate_travel_request(data: Dict) -> Tuple[bool, str]:
    """
    验证旅行请求数据
    Validate Travel Request Data
    
    Args:
        data: 请求数据字典
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误消息)
    """
    # 必填字段检查
    required_fields = ['from_location', 'destination', 'num_people', 'duration']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    # 验证人数
    num_people = data.get('num_people')
    if not isinstance(num_people, int) or num_people < 1:
        return False, "Number of people must be at least 1"
    if num_people > Config.MAX_TRAVELERS:
        return False, f"Number of people cannot exceed {Config.MAX_TRAVELERS}"
    
    # 验证天数
    duration = data.get('duration')
    if not isinstance(duration, int) or duration < 1:
        return False, "Duration must be at least 1 day"
    if duration > Config.MAX_DURATION_DAYS:
        return False, f"Duration cannot exceed {Config.MAX_DURATION_DAYS} days"
    
    # 验证地点
    from_location = data.get('from_location', '').strip()
    destination = data.get('destination', '').strip()
    
    if not from_location:
        return False, "Departure location cannot be empty"
    if not destination:
        return False, "Destination cannot be empty"
    if from_location.lower() == destination.lower():
        return False, "Departure location and destination must be different"
    
    # 验证预算（如果提供）
    if 'budget' in data and data['budget'] is not None:
        budget = data['budget']
        if not isinstance(budget, (int, float)) or budget < 0:
            return False, "Budget must be a positive number"
    
    return True, ""


def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    验证日期范围
    Validate Date Range
    
    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误消息)
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start >= end:
            return False, "Start date must be before end date"
        
        if start < datetime.now():
            return False, "Start date cannot be in the past"
        
        return True, ""
        
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"


def validate_email(email: str) -> Tuple[bool, str]:
    """
    验证邮箱格式
    Validate Email Format
    
    Args:
        email: 邮箱地址
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误消息)
    """
    import re
    
    if not email or not email.strip():
        return False, "Email cannot be empty"
    
    # 简单的邮箱格式验证
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""

