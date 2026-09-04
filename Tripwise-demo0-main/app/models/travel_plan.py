"""
旅行计划数据模型
Travel Plan Data Model

定义旅行计划相关的数据结构和验证逻辑。
Defines travel plan related data structures and validation logic.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime


class TravelPlanRequest(BaseModel):
    """
    旅行计划请求模型
    Travel Plan Request Model
    
    Attributes:
        from_location: 出发地
        destination: 目的地
        num_people: 旅行人数
        duration: 旅行天数
        budget: 预算（可选）
        preferences: 偏好设置（可选）
    """
    from_location: str = Field(..., description="Departure location")
    destination: str = Field(..., description="Destination")
    num_people: int = Field(..., ge=1, le=10, description="Number of travelers")
    duration: int = Field(..., ge=1, le=30, description="Travel duration in days")
    budget: Optional[float] = Field(None, ge=0, description="Budget in CNY")
    preferences: Optional[Dict] = Field(
        default_factory=dict,
        description="Travel preferences (e.g., budget_friendly, luxury, adventure)"
    )
    
    @validator('from_location', 'destination')
    def validate_location(cls, v):
        """验证地点不能为空 Validate location is not empty"""
        if not v or not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "from_location": "北京",
                "destination": "成都",
                "num_people": 2,
                "duration": 5,
                "budget": 5000.0,
                "preferences": {
                    "style": "budget_friendly",
                    "interests": ["food", "culture"]
                }
            }
        }


class FlightOption(BaseModel):
    """航班选项 Flight Option"""
    airline: str = Field(..., description="Airline name")
    departure_time: str = Field(..., description="Departure time")
    arrival_time: str = Field(..., description="Arrival time")
    price: float = Field(..., description="Price per person")
    link: Optional[str] = Field(None, description="Booking link")


class AccommodationOption(BaseModel):
    """住宿选项 Accommodation Option"""
    name: str = Field(..., description="Hotel/Accommodation name")
    address: str = Field(..., description="Address")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Rating")
    price_per_night: float = Field(..., description="Price per night")
    total_price: float = Field(..., description="Total price for duration")
    link: Optional[str] = Field(None, description="Booking link")


class Activity(BaseModel):
    """活动/景点 Activity/Attraction"""
    name: str = Field(..., description="Activity name")
    description: Optional[str] = Field(None, description="Activity description")
    duration: Optional[str] = Field(None, description="Duration")
    price: float = Field(..., description="Price per person")
    location: Optional[str] = Field(None, description="Location")


class DayItinerary(BaseModel):
    """每日行程 Daily Itinerary"""
    day: int = Field(..., description="Day number")
    date: Optional[str] = Field(None, description="Date")
    activities: List[Activity] = Field(default_factory=list, description="List of activities")
    meals: Optional[Dict] = Field(default_factory=dict, description="Meal plans")
    accommodation: Optional[str] = Field(None, description="Accommodation for the night")
    notes: Optional[str] = Field(None, description="Additional notes")


class TravelPlan(BaseModel):
    """
    旅行计划完整模型
    Complete Travel Plan Model
    
    Attributes:
        plan_id: 计划唯一标识符
        user_id: 用户ID
        request: 原始请求信息
        flights: 航班选项列表
        accommodations: 住宿选项列表
        itinerary: 每日行程列表
        total_cost: 总费用估算
        created_at: 创建时间
        status: 计划状态
    """
    plan_id: Optional[str] = Field(None, description="Plan unique identifier")
    user_id: str = Field(..., description="User ID who created the plan")
    request: TravelPlanRequest = Field(..., description="Original travel request")
    flights: List[FlightOption] = Field(default_factory=list, description="Flight options")
    accommodations: List[AccommodationOption] = Field(
        default_factory=list,
        description="Accommodation options"
    )
    itinerary: List[DayItinerary] = Field(default_factory=list, description="Daily itinerary")
    total_cost: Optional[float] = Field(None, description="Estimated total cost")
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Creation timestamp"
    )
    status: str = Field(
        default="pending",
        description="Plan status: pending, processing, completed, failed"
    )
    raw_output: Optional[Dict] = Field(None, description="Raw AI agent output")
    
    class Config:
        json_schema_extra = {
            "example": {
                "plan_id": "plan_12345",
                "user_id": "user_67890",
                "request": {
                    "from_location": "北京",
                    "destination": "成都",
                    "num_people": 2,
                    "duration": 5
                },
                "status": "completed",
                "total_cost": 4500.0
            }
        }

