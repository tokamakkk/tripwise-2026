"""
应用入口文件
Application Entry Point

运行Flask应用的主入口文件。
Main entry point for running the Flask application.

Usage:
    python run.py
    或使用 Flask CLI: flask run
"""

import os
from app import create_app

# 创建应用实例 Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # 从环境变量获取主机和端口配置
    # Get host and port from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting TralP AI Travel Planner on http://{host}:{port}")
    print(f"📝 Debug mode: {debug}")
    print(f"🌍 Environment: {os.getenv('FLASK_ENV', 'development')}")
    
    app.run(host=host, port=port, debug=debug)

