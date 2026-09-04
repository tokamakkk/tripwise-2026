"""
数据模型模块
Data Models Module

定义应用中使用的所有数据模型。
Defines all data models used in the application.
"""

from app.models.user import User
from app.models.travel_plan import TravelPlan, TravelPlanRequest

__all__ = ['User', 'TravelPlan', 'TravelPlanRequest']

