# TralP API 文档

完整的 REST API 参考文档。

## 🌐 基础信息

- **Base URL**: `http://localhost:5000` (开发环境)
- **API Version**: v1
- **Content-Type**: `application/json`
- **认证方式**: Firebase ID Token (Bearer Token)

## 📋 通用响应格式

### 成功响应

```json
{
  "message": "操作成功",
  "data": { ... }
}
```

### 错误响应

```json
{
  "error": "错误类型",
  "message": "错误详细信息"
}
```

## 🔐 认证 API

### 1. 用户注册

创建新用户账号。

**端点**: `POST /api/auth/register`

**请求头**: 无需认证

**请求体**:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "display_name": "张三"  // 可选
}
```

**响应**: `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "uid": "firebase_uid_12345",
    "email": "user@example.com",
    "display_name": "张三"
  }
}
```

**错误响应**:
- `400 Bad Request`: 邮箱已存在或验证失败
- `500 Internal Server Error`: 服务器错误

**示例**:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "display_name": "测试用户"
  }'
```

---

### 2. 验证 Token

验证 Firebase ID token 的有效性。

**端点**: `POST /api/auth/verify`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**响应**: `200 OK`
```json
{
  "valid": true,
  "user": {
    "uid": "firebase_uid_12345",
    "email": "user@example.com",
    "display_name": "张三",
    "email_verified": true
  }
}
```

**错误响应**:
- `401 Unauthorized`: Token 无效或过期

---

### 3. 获取用户资料

获取当前用户的完整资料。

**端点**: `GET /api/auth/profile`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**响应**: `200 OK`
```json
{
  "user": {
    "uid": "firebase_uid_12345",
    "email": "user@example.com",
    "display_name": "张三",
    "created_at": "2025-10-30T12:00:00Z",
    "last_login": "2025-10-30T14:30:00Z",
    "preferences": {
      "currency": "CNY",
      "language": "zh-CN"
    }
  }
}
```

**错误响应**:
- `401 Unauthorized`: 未认证

---

### 4. 更新用户资料

更新用户的显示名称和偏好设置。

**端点**: `PUT /api/auth/profile`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**请求体**:
```json
{
  "display_name": "新名字",  // 可选
  "preferences": {           // 可选
    "currency": "USD",
    "language": "en-US",
    "theme": "dark"
  }
}
```

**响应**: `200 OK`
```json
{
  "message": "Profile updated successfully",
  "user": {
    "uid": "firebase_uid_12345",
    "email": "user@example.com",
    "display_name": "新名字",
    "preferences": {
      "currency": "USD",
      "language": "en-US",
      "theme": "dark"
    }
  }
}
```

**错误响应**:
- `400 Bad Request`: 验证失败
- `401 Unauthorized`: 未认证

---

## ✈️ 旅行规划 API

### 1. 创建旅行计划

提交旅行计划请求，AI 将异步生成完整计划。

**端点**: `POST /api/travel/plan`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
Content-Type: application/json
```

**请求体**:
```json
{
  "from_location": "北京",
  "destination": "成都",
  "num_people": 2,
  "duration": 5,
  "budget": 5000.0,        // 可选，单位：CNY
  "preferences": {          // 可选
    "style": "budget_friendly",
    "interests": ["food", "culture", "nature"]
  }
}
```

**字段说明**:
- `from_location`: 出发地（必填）
- `destination`: 目的地（必填）
- `num_people`: 旅行人数，1-10（必填）
- `duration`: 旅行天数，1-30（必填）
- `budget`: 预算金额（可选）
- `preferences`: 偏好设置（可选）

**响应**: `202 Accepted`
```json
{
  "message": "Travel plan created successfully",
  "plan_id": "plan_abc123",
  "status": "processing",
  "info": "The AI agents are working on your travel plan. Please check back in a moment."
}
```

**错误响应**:
- `400 Bad Request`: 请求参数验证失败
- `401 Unauthorized`: 未认证

**示例**:
```bash
curl -X POST http://localhost:5000/api/travel/plan \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "from_location": "北京",
    "destination": "成都",
    "num_people": 2,
    "duration": 5,
    "budget": 5000
  }'
```

---

### 2. 查询计划状态

查询旅行计划的生成状态（用于轮询）。

**端点**: `GET /api/travel/plans/{plan_id}/status`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**路径参数**:
- `plan_id`: 计划 ID

**响应**: `200 OK`
```json
{
  "plan_id": "plan_abc123",
  "status": "processing",  // pending, processing, completed, failed
  "created_at": "2025-10-30T12:00:00Z",
  "error": null
}
```

**状态说明**:
- `pending`: 等待处理
- `processing`: 正在生成
- `completed`: 生成完成
- `failed`: 生成失败

**错误响应**:
- `404 Not Found`: 计划不存在
- `401 Unauthorized`: 未认证

**轮询示例**:
```bash
while true; do
  curl http://localhost:5000/api/travel/plans/plan_abc123/status \
    -H "Authorization: Bearer YOUR_TOKEN"
  sleep 5
done
```

---

### 3. 获取完整计划

获取已生成的完整旅行计划。

**端点**: `GET /api/travel/plans/{plan_id}`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**路径参数**:
- `plan_id`: 计划 ID

**响应**: `200 OK`
```json
{
  "plan": {
    "plan_id": "plan_abc123",
    "user_id": "firebase_uid_12345",
    "status": "completed",
    "created_at": "2025-10-30T12:00:00Z",
    "request": {
      "from_location": "北京",
      "destination": "成都",
      "num_people": 2,
      "duration": 5,
      "budget": 5000
    },
    "flights": [
      {
        "airline": "中国国际航空",
        "departure_time": "2025-11-01 08:00",
        "arrival_time": "2025-11-01 11:00",
        "price": 800,
        "link": "https://booking.example.com/..."
      }
    ],
    "accommodations": [
      {
        "name": "锦江酒店",
        "address": "成都市锦江区...",
        "rating": 4.5,
        "price_per_night": 300,
        "total_price": 1500,
        "link": "https://booking.example.com/..."
      }
    ],
    "itinerary": [
      {
        "day": 1,
        "date": "2025-11-01",
        "activities": [
          {
            "name": "宽窄巷子",
            "description": "成都著名景点",
            "duration": "2小时",
            "price": 0,
            "location": "成都市青羊区"
          }
        ],
        "meals": {
          "lunch": "陈麻婆豆腐",
          "dinner": "火锅"
        },
        "accommodation": "锦江酒店",
        "notes": "第一天轻松游览"
      }
    ],
    "total_cost": 4500,
    "parsed_result": {
      "planning_result": "详细的规划结果文本...",
      "itinerary_result": "详细的行程安排文本..."
    },
    "raw_output": "AI 原始输出..."
  }
}
```

**错误响应**:
- `404 Not Found`: 计划不存在
- `401 Unauthorized`: 未认证

---

### 4. 获取所有计划

获取当前用户的所有旅行计划列表。

**端点**: `GET /api/travel/plans`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**响应**: `200 OK`
```json
{
  "plans": [
    {
      "plan_id": "plan_abc123",
      "status": "completed",
      "created_at": "2025-10-30T12:00:00Z",
      "request": {
        "from_location": "北京",
        "destination": "成都",
        "num_people": 2,
        "duration": 5
      }
    },
    {
      "plan_id": "plan_xyz789",
      "status": "processing",
      "created_at": "2025-10-31T10:00:00Z",
      "request": {
        "from_location": "上海",
        "destination": "杭州",
        "num_people": 4,
        "duration": 3
      }
    }
  ],
  "count": 2
}
```

**错误响应**:
- `401 Unauthorized`: 未认证

---

### 5. 删除计划

删除指定的旅行计划。

**端点**: `DELETE /api/travel/plans/{plan_id}`

**请求头**:
```
Authorization: Bearer <firebase_id_token>
```

**路径参数**:
- `plan_id`: 计划 ID

**响应**: `200 OK`
```json
{
  "message": "Travel plan deleted successfully"
}
```

**错误响应**:
- `404 Not Found`: 计划不存在
- `401 Unauthorized`: 未认证

---

## 🏥 健康检查

### 健康检查端点

检查 API 服务是否正常运行。

**端点**: `GET /health`

**请求头**: 无需认证

**响应**: `200 OK`
```json
{
  "status": "healthy",
  "message": "TralP API is running"
}
```

---

## 📊 HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 OK | 请求成功 |
| 201 Created | 资源创建成功 |
| 202 Accepted | 请求已接受，异步处理中 |
| 400 Bad Request | 请求参数错误 |
| 401 Unauthorized | 未认证或认证失败 |
| 403 Forbidden | 无权限访问 |
| 404 Not Found | 资源不存在 |
| 500 Internal Server Error | 服务器内部错误 |

---

## 🔒 认证流程

### 完整认证流程

1. **客户端注册**
   ```bash
   POST /api/auth/register
   ```

2. **使用 Firebase SDK 登录**（客户端）
   ```javascript
   import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
   
   const auth = getAuth();
   signInWithEmailAndPassword(auth, email, password)
     .then((userCredential) => {
       userCredential.user.getIdToken().then((token) => {
         // 使用此 token 调用 API
       });
     });
   ```

3. **在 API 请求中使用 Token**
   ```bash
   curl http://localhost:5000/api/travel/plan \
     -H "Authorization: Bearer <firebase_id_token>"
   ```

---

## 💡 使用示例

### Python 示例

```python
import requests
import time

BASE_URL = "http://localhost:5000"

# 1. 注册
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "user@example.com",
    "password": "password123",
    "display_name": "张三"
})
print(response.json())

# 2. 获取 token（需要使用 Firebase SDK）
# token = get_firebase_token()

# 3. 创建旅行计划
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/api/travel/plan",
    headers=headers,
    json={
        "from_location": "北京",
        "destination": "成都",
        "num_people": 2,
        "duration": 5
    }
)
plan_data = response.json()
plan_id = plan_data['plan_id']

# 4. 轮询状态
while True:
    response = requests.get(
        f"{BASE_URL}/api/travel/plans/{plan_id}/status",
        headers=headers
    )
    status = response.json()
    if status['status'] in ['completed', 'failed']:
        break
    print(f"状态: {status['status']}")
    time.sleep(5)

# 5. 获取完整计划
response = requests.get(
    f"{BASE_URL}/api/travel/plans/{plan_id}",
    headers=headers
)
plan = response.json()
print(plan)
```

### JavaScript 示例

```javascript
const BASE_URL = 'http://localhost:5000';

// 使用 Firebase 获取 token
import { getAuth } from 'firebase/auth';

const auth = getAuth();
const token = await auth.currentUser.getIdToken();

// 创建旅行计划
const response = await fetch(`${BASE_URL}/api/travel/plan`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    from_location: '北京',
    destination: '成都',
    num_people: 2,
    duration: 5,
    budget: 5000
  })
});

const data = await response.json();
console.log('Plan ID:', data.plan_id);

// 轮询状态
const pollStatus = async (planId) => {
  const response = await fetch(
    `${BASE_URL}/api/travel/plans/${planId}/status`,
    {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  const status = await response.json();
  return status;
};
```

---

## 🚨 错误处理

### 常见错误

#### 1. 未认证
```json
{
  "error": "Unauthorized",
  "message": "No authorization header provided"
}
```

**解决**: 在请求头中添加 `Authorization: Bearer <token>`

#### 2. Token 无效
```json
{
  "error": "Unauthorized",
  "message": "Invalid token"
}
```

**解决**: 使用 Firebase SDK 重新获取有效的 token

#### 3. 验证失败
```json
{
  "error": "Validation Error",
  "details": [
    {
      "loc": ["num_people"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error"
    }
  ]
}
```

**解决**: 检查请求参数是否符合要求

---

## 📝 备注

1. **异步处理**: 旅行计划生成是异步的，需要轮询状态
2. **Token 过期**: Firebase ID token 有效期为 1 小时，过期后需要刷新
3. **速率限制**: 建议轮询间隔至少 3-5 秒
4. **第三方 API**: 高德地图和携程 API 需要配置相应的密钥

---

## 🔗 相关链接

- [项目主文档](README.md)
- [快速启动指南](QUICKSTART.md)
- [项目结构说明](STRUCTURE.md)
- [Firebase 文档](https://firebase.google.com/docs)
- [CrewAI 文档](https://docs.crewai.com/)

