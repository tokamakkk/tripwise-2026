"""
配置管理模块
Configuration Management Module

该模块负责加载和管理应用的所有配置信息，包括Flask配置、Firebase配置、LLM配置和第三方API配置。
This module handles loading and managing all application configurations.
"""

import os
from dotenv import load_dotenv

# 加载环境变量 Load environment variables
load_dotenv()


class Config:
    """
    基础配置类
    Base Configuration Class
    
    Attributes:
        SECRET_KEY: Flask应用密钥
        DEBUG: 调试模式开关
        FIREBASE_CONFIG: Firebase配置字典
        LLM_CONFIG: LLM模型配置字典
        API_KEYS: 第三方API密钥字典
    """
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Firebase 配置
    FIREBASE_CONFIG = {
        'apiKey': os.getenv('FIREBASE_API_KEY'),
        'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
        'projectId': os.getenv('FIREBASE_PROJECT_ID'),
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.getenv('FIREBASE_APP_ID'),
    }
    
    # Firebase Admin SDK 配置
    FIREBASE_ADMIN_CREDENTIALS_PATH = os.getenv(
        'FIREBASE_ADMIN_CREDENTIALS_PATH',
        './firebase-admin-sdk.json'
    )
    
    # LLM 配置
    LLM_CONFIG = {
        'model': os.getenv('LLM_MODEL', 'ollama/llama3.2:1b'),
        'base_url': os.getenv('LLM_BASE_URL', 'http://127.0.0.1:11434'),
        'provider': os.getenv('LLM_PROVIDER', 'ollama'),
    }
    
    # 第三方 API 密钥
    API_KEYS = {
        'serper': os.getenv('SERPER_API_KEY'),
        'amap': os.getenv('AMAP_API_KEY'),
        'ctrip': {
            'key': os.getenv('CTRIP_API_KEY'),
            'secret': os.getenv('CTRIP_API_SECRET'),
        }
    }
    
    # 应用设置
    MAX_TRAVELERS = int(os.getenv('MAX_TRAVELERS', 10))
    MAX_DURATION_DAYS = int(os.getenv('MAX_DURATION_DAYS', 30))
    DEFAULT_DURATION_DAYS = int(os.getenv('DEFAULT_DURATION_DAYS', 7))


class DevelopmentConfig(Config):
    """开发环境配置 Development Configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生产环境配置 Production Configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """测试环境配置 Testing Configuration"""
    DEBUG = True
    TESTING = True


# 配置字典 Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name=None):
    """
    获取配置对象
    Get configuration object
    
    Args:
        env_name: 环境名称 (development, production, testing)
        
    Returns:
        Config: 配置对象实例
    """
    if env_name is None:
        env_name = os.getenv('FLASK_ENV', 'development')
    return config.get(env_name, config['default'])

