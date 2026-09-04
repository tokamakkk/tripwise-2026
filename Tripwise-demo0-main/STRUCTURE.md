# TralP 项目结构详解

本文档详细说明项目的目录结构和各文件的作用。

## 📁 完整目录树

```
TralP/
│
├── app/                                # 应用主目录
│   ├── __init__.py                    # Flask 应用工厂，创建和配置 Flask app
│   ├── config.py                      # 配置管理（开发/生产/测试环境）
│   │
│   ├── models/                        # 数据模型层（Pydantic）
│   │   ├── __init__.py               # 导出所有模型
│   │   ├── user.py                   # 用户模型（User, UserLogin, UserRegister）
│   │   ├── travel_plan.py            # 旅行计划模型（TravelPlan, FlightOption 等）
│   │   └── README.md                 # 模型文档
│   │
│   ├── routes/                        # API 路由层
│   │   ├── __init__.py               # 导出所有蓝图
│   │   ├── auth.py                   # 认证路由（注册、登录、资料）
│   │   ├── travel.py                 # 旅行规划路由（创建、查询、删除计划）
│   │   └── README.md                 # 路由文档
│   │
│   ├── services/                      # 业务逻辑层
│   │   ├── __init__.py               # 导出主要服务
│   │   ├── firebase_service.py       # Firebase 认证和数据库服务
│   │   ├── ai_service.py             # AI 服务（协调 CrewAI agents）
│   │   ├── README.md                 # 服务文档
│   │   │
│   │   └── third_party/              # 第三方 API 集成
│   │       ├── __init__.py           # 导出第三方服务
│   │       ├── amap_service.py       # 高德地图 API（地理编码、POI、路线）
│   │       ├── ctrip_service.py      # 携程旅行 API（酒店、航班、景点）
│   │       └── README.md             # 第三方 API 文档
│   │
│   ├── agents/                        # CrewAI Agents 定义
│   │   ├── __init__.py               # 导出 agent 创建函数
│   │   ├── planner_agent.py          # 旅行规划 Agent（研究航班、酒店、活动）
│   │   ├── writer_agent.py           # 行程编写 Agent（生成详细行程）
│   │   └── README.md                 # Agents 文档
│   │
│   ├── tools/                         # AI Tools（供 Agents 使用）
│   │   ├── __init__.py               # 导出所有工具
│   │   ├── search_tool.py            # 互联网搜索工具（Serper API）
│   │   └── README.md                 # Tools 文档
│   │
│   └── utils/                         # 工具函数
│       ├── __init__.py               # 导出常用工具
│       ├── decorators.py             # 装饰器（@require_auth, @handle_errors）
│       ├── validators.py             # 验证器（数据验证函数）
│       └── README.md                 # Utils 文档
│
├── tests/                             # 测试目录
│   ├── __init__.py                   # 测试模块初始化
│   ├── test_services.py              # 服务层测试
│   └── README.md                     # 测试文档
│
├── static/                            # 静态资源目录
│   ├── css/                          # CSS 样式
│   ├── js/                           # JavaScript 文件
│   └── images/                       # 图片资源
│
├── templates/                         # HTML 模板目录
│
├── requirements.txt                   # Python 依赖列表
├── .env.example                      # 环境变量示例
├── .gitignore                        # Git 忽略文件
├── run.py                            # 应用启动入口
├── README.md                         # 项目主文档
└── STRUCTURE.md                      # 本文档（项目结构说明）
```

## 🔑 核心文件说明

### 应用入口

- **run.py**
  - 应用启动入口
  - 创建 Flask app 实例
  - 配置主机、端口、调试模式
  - 运行命令：`python run.py`

### 配置文件

- **app/config.py**
  - 定义配置类：`DevelopmentConfig`, `ProductionConfig`, `TestingConfig`
  - 管理环境变量
  - 配置 Firebase、LLM、第三方 API

- **.env.example**
  - 环境变量模板
  - 复制为 `.env` 并填入实际值
  - 包含所有必需的配置项

- **requirements.txt**
  - Python 依赖包列表
  - 安装命令：`pip install -r requirements.txt`

### 应用初始化

- **app/__init__.py**
  - Flask 应用工厂函数 `create_app()`
  - 注册蓝图
  - 配置 CORS
  - 注册错误处理器

## 📊 数据流图

### 用户认证流程

```
Client
  ↓ (注册/登录)
Firebase Authentication (客户端 SDK)
  ↓ (获取 ID Token)
Client
  ↓ (带 Token 的 API 请求)
Flask Route (@require_auth)
  ↓ (验证 Token)
FirebaseService.verify_token()
  ↓ (Token 有效)
Route Handler (g.user_id 可用)
  ↓ (处理业务逻辑)
Response
```

### 旅行计划生成流程

```
Client
  ↓ (POST /api/travel/plan)
travel.py (create_travel_plan)
  ↓ (验证并保存初始计划)
FirebaseService.save_travel_plan()
  ↓ (调用 AI 服务)
AIService.generate_travel_plan()
  ↓ (创建 Agents 和 Tasks)
Planner Agent → Research (SearchTool)
  ↓ (输出：航班、酒店、活动选项)
Writer Agent → Create Itinerary
  ↓ (输出：完整行程)
CrewAI Result
  ↓ (解析并保存)
FirebaseService.update_travel_plan()
  ↓ (返回结果)
Client (轮询状态或获取完整计划)
```

## 🔌 扩展点

### 1. 添加新的数据模型

位置：`app/models/`

```python
# app/models/booking.py
from pydantic import BaseModel

class Booking(BaseModel):
    booking_id: str
    user_id: str
    # ... 其他字段
```

在 `app/models/__init__.py` 中导出。

### 2. 添加新的 API 路由

位置：`app/routes/`

```python
# app/routes/booking.py
from flask import Blueprint

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/create', methods=['POST'])
@require_auth
def create_booking():
    # ... 实现
    pass
```

在 `app/__init__.py` 中注册蓝图。

### 3. 添加新的第三方服务

位置：`app/services/third_party/`

```python
# app/services/third_party/booking_service.py
class BookingService:
    def __init__(self):
        self.api_key = Config.API_KEYS.get('booking')
    
    def search_hotels(self, city):
        # ... 实现
        pass
```

在 `app/services/third_party/__init__.py` 中导出。

### 4. 添加新的 AI Agent

位置：`app/agents/`

```python
# app/agents/budget_agent.py
def create_budget_optimizer(budget: float) -> Agent:
    return Agent(
        role='Budget Optimizer',
        goal=f'Optimize travel plan within budget of {budget}',
        # ... 配置
    )
```

在 `app/agents/__init__.py` 中导出。

### 5. 添加新的 AI Tool

位置：`app/tools/`

```python
# app/tools/price_comparison_tool.py
from crewai.tools import BaseTool

class PriceComparisonTool(BaseTool):
    name: str = "Compare Prices"
    
    def _run(self, item: str) -> List[Dict]:
        # ... 实现
        pass
```

在 `app/tools/__init__.py` 中导出。

## 🎯 模块职责划分

### Models（数据模型）
- **职责**：定义数据结构和验证规则
- **不做**：业务逻辑、数据库操作
- **使用**：Pydantic 进行数据验证

### Routes（路由）
- **职责**：处理 HTTP 请求和响应
- **不做**：复杂业务逻辑、直接数据库操作
- **使用**：调用 Services 层处理业务

### Services（服务）
- **职责**：业务逻辑、外部服务调用
- **不做**：HTTP 请求处理、路由定义
- **使用**：被 Routes 层调用

### Agents（AI Agents）
- **职责**：定义 AI agent 的角色和任务
- **不做**：HTTP 请求处理、数据存储
- **使用**：由 AIService 协调执行

### Tools（AI Tools）
- **职责**：为 Agents 提供工具能力
- **不做**：独立运行、直接被路由调用
- **使用**：在 Agents 的 tools 列表中

### Utils（工具）
- **职责**：通用工具函数、装饰器
- **不做**：业务逻辑
- **使用**：被各层模块调用

## 🔐 安全考虑

### 认证和授权
- 使用 Firebase Authentication 进行用户认证
- 所有需要认证的路由使用 `@require_auth` 装饰器
- Token 在 Authorization header 中传递

### 数据验证
- 使用 Pydantic 进行数据验证
- 在 Utils 层提供额外验证函数
- 验证失败返回 400 Bad Request

### 错误处理
- 使用 `@handle_errors` 装饰器统一处理错误
- 不向客户端暴露敏感错误信息
- 记录详细错误日志供调试

### API 密钥管理
- 所有密钥存储在 `.env` 文件中
- `.env` 文件在 `.gitignore` 中
- 生产环境使用环境变量或密钥管理服务

## 📈 性能优化建议

### 异步处理
- 旅行计划生成使用异步处理
- 考虑使用 Celery 或 RQ 实现任务队列
- 客户端轮询状态或使用 WebSocket

### 缓存
- 缓存常用的第三方 API 结果
- 使用 Redis 缓存会话数据
- 实现查询结果缓存

### 数据库优化
- Firebase Realtime Database 使用合理的数据结构
- 避免深度嵌套
- 使用索引加速查询

## 🧪 测试策略

### 单元测试
- 测试独立函数和类方法
- Mock 外部依赖
- 覆盖边界情况

### 集成测试
- 测试多个模块协作
- 测试 API 端点
- 使用测试数据库

### 端到端测试
- 模拟真实用户流程
- 测试完整的用户旅程
- 验证系统整体功能

## 📚 相关文档

- [README.md](README.md) - 项目主文档
- [app/models/README.md](app/models/README.md) - 数据模型文档
- [app/services/README.md](app/services/README.md) - 服务层文档
- [app/agents/README.md](app/agents/README.md) - AI Agents 文档
- [app/routes/README.md](app/routes/README.md) - API 路由文档
- [tests/README.md](tests/README.md) - 测试文档

