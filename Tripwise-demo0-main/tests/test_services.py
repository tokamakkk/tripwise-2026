"""
服务层测试
Services Layer Tests

测试 Firebase 服务、AI 服务和第三方 API 服务。
Tests for Firebase service, AI service, and third-party API services.
"""

import pytest
from app.services.firebase_service import FirebaseService
from app.models.travel_plan import TravelPlanRequest


class TestFirebaseService:
    """Firebase 服务测试"""
    
    def test_init_firebase(self):
        """测试 Firebase 初始化"""
        # Firebase 在导入时已初始化
        assert FirebaseService._initialized is True
    
    # 注意：以下测试需要实际的 Firebase 凭证
    # 在 CI/CD 环境中应使用 mock
    
    # def test_verify_token(self):
    #     """测试 token 验证"""
    #     # 需要有效的 token
    #     pass
    
    # def test_create_user(self):
    #     """测试创建用户"""
    #     pass


class TestAIService:
    """AI 服务测试"""
    
    # 注意：AI 服务测试耗时较长，建议使用 mock
    
    # def test_generate_travel_plan(self):
    #     """测试生成旅行计划"""
    #     request = TravelPlanRequest(
    #         from_location="北京",
    #         destination="成都",
    #         num_people=2,
    #         duration=5
    #     )
    #     # 使用 mock LLM 测试
    #     pass


# 运行测试：pytest tests/

