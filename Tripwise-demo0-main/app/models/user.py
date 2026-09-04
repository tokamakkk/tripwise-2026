"""
用户数据模型
User Data Model

定义用户相关的数据结构和验证逻辑。
Defines user-related data structures and validation logic.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """
    用户模型
    User Model
    
    Attributes:
        uid: Firebase用户唯一标识符
        email: 用户邮箱
        display_name: 用户显示名称
        created_at: 账户创建时间
        last_login: 最后登录时间
        preferences: 用户偏好设置（JSON）
    """
    uid: str = Field(..., description="Firebase user unique identifier")
    email: EmailStr = Field(..., description="User email address")
    display_name: Optional[str] = Field(None, description="User display name")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_login: Optional[str] = Field(None, description="Last login timestamp")
    preferences: Optional[dict] = Field(default_factory=dict, description="User preferences")
    
    class Config:
        """Pydantic配置"""
        json_schema_extra = {
            "example": {
                "uid": "firebase_uid_12345",
                "email": "user@example.com",
                "display_name": "John Doe",
                "created_at": "2025-10-30T12:00:00Z",
                "preferences": {
                    "currency": "CNY",
                    "language": "zh-CN"
                }
            }
        }


class UserLogin(BaseModel):
    """
    用户登录请求模型
    User Login Request Model
    
    Attributes:
        email: 用户邮箱
        password: 用户密码
    """
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")


class UserRegister(BaseModel):
    """
    用户注册请求模型
    User Registration Request Model
    
    Attributes:
        email: 用户邮箱
        password: 用户密码
        display_name: 用户显示名称
    """
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="User password")
    display_name: Optional[str] = Field(None, description="User display name")


class UserProfile(BaseModel):
    """
    用户资料更新模型
    User Profile Update Model
    
    Attributes:
        display_name: 用户显示名称
        preferences: 用户偏好设置
    """
    display_name: Optional[str] = Field(None, description="User display name")
    preferences: Optional[dict] = Field(None, description="User preferences")

