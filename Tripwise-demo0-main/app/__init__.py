"""
Flask应用工厂模块
Flask Application Factory Module

该模块负责创建和配置Flask应用实例，注册蓝图，初始化扩展。
This module creates and configures the Flask application instance.
"""

from flask import Flask
from flask_cors import CORS
from app.config import get_config


def create_app(config_name=None):
    """
    应用工厂函数
    Application Factory Function
    
    Args:
        config_name: 配置环境名称 (development, production, testing)
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置 Load configuration
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)
    
    # 启用CORS Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册蓝图 Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.travel import travel_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(travel_bp, url_prefix='/api/travel')
    
    # 注册错误处理器 Register error handlers
    register_error_handlers(app)
    
    # 健康检查端点 Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'TralP API is running'}, 200
    
    @app.route('/')
    def index():
        return {
            'name': 'TralP - AI Travel Planner API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'auth': '/api/auth',
                'travel': '/api/travel',
            }
        }, 200
    
    return app


def register_error_handlers(app):
    """
    注册全局错误处理器
    Register Global Error Handlers
    
    Args:
        app: Flask应用实例
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad Request', 'message': str(error)}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized', 'message': 'Authentication required'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden', 'message': str(error)}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not Found', 'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal Server Error', 'message': str(error)}, 500

