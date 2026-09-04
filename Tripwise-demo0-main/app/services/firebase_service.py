"""
Firebase服务模块
Firebase Service Module

负责Firebase认证和Realtime Database的所有操作。
Handles all Firebase authentication and Realtime Database operations.

Functions:
    - init_firebase(): 初始化Firebase Admin SDK
    - verify_token(token): 验证Firebase ID token
    - create_user(email, password): 创建新用户
    - get_user(uid): 获取用户信息
    - update_user(uid, data): 更新用户信息
    - save_travel_plan(user_id, plan): 保存旅行计划
    - get_travel_plans(user_id): 获取用户的所有旅行计划
    - get_travel_plan(plan_id): 获取特定旅行计划
"""

import firebase_admin
from firebase_admin import credentials, auth, db
from typing import Optional, Dict, List
from app.config import Config
import os


class FirebaseService:
    """
    Firebase服务类
    Firebase Service Class
    
    提供Firebase认证和数据库操作的统一接口。
    Provides unified interface for Firebase auth and database operations.
    """
    
    _initialized = False
    
    @classmethod
    def init_firebase(cls):
        """
        初始化Firebase Admin SDK
        Initialize Firebase Admin SDK
        
        只初始化一次，避免重复初始化。
        Initializes only once to avoid duplicate initialization.
        """
        if cls._initialized:
            return
        
        try:
            # 检查凭证文件是否存在
            cred_path = Config.FIREBASE_ADMIN_CREDENTIALS_PATH
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': Config.FIREBASE_CONFIG['databaseURL']
                })
            else:
                # 如果没有凭证文件，使用默认凭证（适用于Cloud环境）
                firebase_admin.initialize_app(options={
                    'databaseURL': Config.FIREBASE_CONFIG['databaseURL']
                })
            
            cls._initialized = True
            print("✅ Firebase initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Firebase: {e}")
            raise
    
    @staticmethod
    def verify_token(id_token: str) -> Dict:
        """
        验证Firebase ID token
        Verify Firebase ID Token
        
        Args:
            id_token: Firebase ID token from client
            
        Returns:
            Dict: 解码后的token信息，包含uid等
            
        Raises:
            ValueError: Token无效时抛出
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")
    
    @staticmethod
    def create_user(email: str, password: str, display_name: Optional[str] = None) -> Dict:
        """
        创建新用户
        Create New User
        
        Args:
            email: 用户邮箱
            password: 用户密码
            display_name: 用户显示名称（可选）
            
        Returns:
            Dict: 用户信息
        """
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name
            }
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")
    
    @staticmethod
    def get_user(uid: str) -> Dict:
        """
        获取用户信息
        Get User Information
        
        Args:
            uid: 用户唯一标识符
            
        Returns:
            Dict: 用户信息
        """
        try:
            user = auth.get_user(uid)
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'email_verified': user.email_verified
            }
        except Exception as e:
            raise ValueError(f"Error getting user: {str(e)}")
    
    @staticmethod
    def update_user_data(uid: str, data: Dict) -> Dict:
        """
        更新用户数据到Realtime Database
        Update User Data to Realtime Database
        
        Args:
            uid: 用户唯一标识符
            data: 要更新的数据
            
        Returns:
            Dict: 更新后的数据
        """
        try:
            ref = db.reference(f'users/{uid}')
            ref.update(data)
            return ref.get()
        except Exception as e:
            raise ValueError(f"Error updating user data: {str(e)}")
    
    @staticmethod
    def get_user_data(uid: str) -> Optional[Dict]:
        """
        从Realtime Database获取用户数据
        Get User Data from Realtime Database
        
        Args:
            uid: 用户唯一标识符
            
        Returns:
            Dict: 用户数据，如果不存在返回None
        """
        try:
            ref = db.reference(f'users/{uid}')
            return ref.get()
        except Exception as e:
            raise ValueError(f"Error getting user data: {str(e)}")
    
    @staticmethod
    def save_travel_plan(user_id: str, plan_data: Dict) -> str:
        """
        保存旅行计划
        Save Travel Plan
        
        Args:
            user_id: 用户ID
            plan_data: 旅行计划数据
            
        Returns:
            str: 计划ID
        """
        try:
            ref = db.reference(f'travel_plans/{user_id}')
            new_plan_ref = ref.push(plan_data)
            plan_id = new_plan_ref.key
            
            # 更新plan_id字段
            new_plan_ref.update({'plan_id': plan_id})
            
            return plan_id
        except Exception as e:
            raise ValueError(f"Error saving travel plan: {str(e)}")
    
    @staticmethod
    def get_travel_plans(user_id: str) -> List[Dict]:
        """
        获取用户的所有旅行计划
        Get All Travel Plans for User
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[Dict]: 旅行计划列表
        """
        try:
            ref = db.reference(f'travel_plans/{user_id}')
            plans = ref.get()
            
            if not plans:
                return []
            
            # 转换为列表格式
            return [plan for plan in plans.values()]
        except Exception as e:
            raise ValueError(f"Error getting travel plans: {str(e)}")
    
    @staticmethod
    def get_travel_plan(user_id: str, plan_id: str) -> Optional[Dict]:
        """
        获取特定旅行计划
        Get Specific Travel Plan
        
        Args:
            user_id: 用户ID
            plan_id: 计划ID
            
        Returns:
            Dict: 旅行计划数据，如果不存在返回None
        """
        try:
            ref = db.reference(f'travel_plans/{user_id}/{plan_id}')
            return ref.get()
        except Exception as e:
            raise ValueError(f"Error getting travel plan: {str(e)}")
    
    @staticmethod
    def update_travel_plan(user_id: str, plan_id: str, data: Dict) -> Dict:
        """
        更新旅行计划
        Update Travel Plan
        
        Args:
            user_id: 用户ID
            plan_id: 计划ID
            data: 要更新的数据
            
        Returns:
            Dict: 更新后的数据
        """
        try:
            ref = db.reference(f'travel_plans/{user_id}/{plan_id}')
            ref.update(data)
            return ref.get()
        except Exception as e:
            raise ValueError(f"Error updating travel plan: {str(e)}")
    
    @staticmethod
    def delete_travel_plan(user_id: str, plan_id: str) -> bool:
        """
        删除旅行计划
        Delete Travel Plan
        
        Args:
            user_id: 用户ID
            plan_id: 计划ID
            
        Returns:
            bool: 删除成功返回True
        """
        try:
            ref = db.reference(f'travel_plans/{user_id}/{plan_id}')
            ref.delete()
            return True
        except Exception as e:
            raise ValueError(f"Error deleting travel plan: {str(e)}")


# 初始化Firebase
FirebaseService.init_firebase()

