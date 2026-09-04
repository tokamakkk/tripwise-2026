# Routes 模块

API 路由定义模块，处理所有 HTTP 请求。

## 文件说明

### `__init__.py`
模块初始化文件，导出所有蓝图。

### `auth.py`
认证相关路由。

#### Blueprint 信息
- 名称：`auth_bp`
- URL 前缀：`/api/auth`

#### 端点（Endpoints）

1. **POST /api/auth/register**
   - 功能：用户注册
   - 认证：不需要
   - 请求体：
     ```json
     {
       "email": "user@example.com",
       "password": "password123",
       "display_name": "John Doe"  // 可选
     }
     ```
   - 响应：
     - 201 Created：注册成功
     - 400 Bad Request：验证失败或邮箱已存在

2. **POST /api/auth/login**
   - 功能：用户登录说明
   - 认证：不需要
   - 说明：实际登录通过 Firebase SDK 在客户端完成
   - 响应：
     - 200 OK：返回使用说明

3. **POST /api/auth/verify**
   - 功能：验证 Firebase ID token
   - 认证：需要（Authorization header）
   - Headers：
     ```
     Authorization: Bearer <firebase_id_token>
     ```
   - 响应：
     - 200 OK：Token 有效，返回用户信息
     - 401 Unauthorized：Token 无效

4. **GET /api/auth/profile**
   - 功能：获取用户资料
   - 认证：需要
   - 装饰器：`@require_auth`
   - 响应：
     - 200 OK：返回用户资料
     - 401 Unauthorized：未认证

5. **PUT /api/auth/profile**
   - 功能：更新用户资料
   - 认证：需要
   - 装饰器：`@require_auth`
   - 请求体：
     ```json
     {
       "display_name": "New Name",
       "preferences": {
         "currency": "CNY",
         "language": "zh-CN"
       }
     }
     ```
   - 响应：
     - 200 OK：更新成功
     - 400 Bad Request：验证失败
     - 401 Unauthorized：未认证

### `travel.py`
旅行规划相关路由。

#### Blueprint 信息
- 名称：`travel_bp`
- URL 前缀：`/api/travel`

#### 端点（Endpoints）

1. **POST /api/travel/plan**
   - 功能：创建旅行计划
   - 认证：需要
   - 装饰器：`@require_auth`
   - 请求体：
     ```json
     {
       "from_location": "北京",
       "destination": "成都",
       "num_people": 2,
       "duration": 5,
       "budget": 5000.0,  // 可选
       "preferences": {}  // 可选
     }
     ```
   - 响应：
     - 202 Accepted：计划创建成功，正在处理
     - 400 Bad Request：验证失败
     - 401 Unauthorized：未认证
   - 说明：异步处理，使用 status 端点查询进度

2. **GET /api/travel/plans**
   - 功能：获取用户的所有旅行计划
   - 认证：需要
   - 装饰器：`@require_auth`
   - 响应：
     ```json
     {
       "plans": [
         {
           "plan_id": "...",
           "status": "completed",
           "created_at": "...",
           "request": {...}
         }
       ],
       "count": 5
     }
     ```
   - 响应码：
     - 200 OK：成功
     - 401 Unauthorized：未认证

3. **GET /api/travel/plans/<plan_id>**
   - 功能：获取特定旅行计划详情
   - 认证：需要
   - 装饰器：`@require_auth`
   - 路径参数：
     - `plan_id: str` - 计划ID
   - 响应：
     - 200 OK：返回完整计划
     - 404 Not Found：计划不存在
     - 401 Unauthorized：未认证

4. **GET /api/travel/plans/<plan_id>/status**
   - 功能：获取旅行计划生成状态
   - 认证：需要
   - 装饰器：`@require_auth`
   - 路径参数：
     - `plan_id: str` - 计划ID
   - 响应：
     ```json
     {
       "plan_id": "...",
       "status": "processing",  // pending/processing/completed/failed
       "created_at": "...",
       "error": null
     }
     ```
   - 响应码：
     - 200 OK：成功
     - 404 Not Found：计划不存在
     - 401 Unauthorized：未认证
   - 说明：用于轮询检查计划生成进度

5. **DELETE /api/travel/plans/<plan_id>**
   - 功能：删除旅行计划
   - 认证：需要
   - 装饰器：`@require_auth`
   - 路径参数：
     - `plan_id: str` - 计划ID
   - 响应：
     - 200 OK：删除成功
     - 404 Not Found：计划不存在
     - 401 Unauthorized：未认证

## 使用示例

### 完整流程示例

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. 注册用户
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "user@example.com",
    "password": "password123",
    "display_name": "张三"
})
print(response.json())

# 2. 在客户端使用 Firebase SDK 登录获取 ID token
# firebase.auth().signInWithEmailAndPassword(email, password)
# id_token = await user.getIdToken()

# 3. 创建旅行计划
headers = {"Authorization": f"Bearer {id_token}"}
response = requests.post(f"{BASE_URL}/api/travel/plan", 
    headers=headers,
    json={
        "from_location": "北京",
        "destination": "成都",
        "num_people": 2,
        "duration": 5
    }
)
plan = response.json()
plan_id = plan['plan_id']

# 4. 轮询检查状态
import time
while True:
    response = requests.get(
        f"{BASE_URL}/api/travel/plans/{plan_id}/status",
        headers=headers
    )
    status = response.json()
    if status['status'] in ['completed', 'failed']:
        break
    time.sleep(5)

# 5. 获取完整计划
response = requests.get(
    f"{BASE_URL}/api/travel/plans/{plan_id}",
    headers=headers
)
full_plan = response.json()
print(full_plan)
```

## 错误处理

所有路由使用 `@handle_errors` 装饰器统一处理错误：

- `ValueError` → 400 Bad Request
- `PermissionError` → 403 Forbidden
- 其他异常 → 500 Internal Server Error

## 认证机制

使用 `@require_auth` 装饰器验证 Firebase ID token：

1. 从 `Authorization` header 提取 token
2. 使用 Firebase Admin SDK 验证 token
3. 将用户信息存储在 `flask.g` 对象中
4. 在路由函数中通过 `g.user_id` 访问

## 扩展指南

### 添加新路由

1. 在现有文件或新文件中定义路由
2. 使用装饰器：
   - `@require_auth` - 需要认证
   - `@handle_errors` - 错误处理
3. 在 `app/__init__.py` 中注册蓝图
4. 添加到此 README 的文档中

