# Services 模块

业务逻辑和外部服务封装层。

## 文件说明

### `__init__.py`
模块初始化文件，导出主要服务类。

### `firebase_service.py`
Firebase 认证和 Realtime Database 服务。

#### 类定义（Classes）

**FirebaseService**
- Firebase 服务统一接口类

#### 类方法（Class Methods）

1. **init_firebase()**
   - 初始化 Firebase Admin SDK
   - 只初始化一次，避免重复
   - 无参数
   - 返回：None

#### 静态方法（Static Methods）

1. **verify_token(id_token: str) -> Dict**
   - 验证 Firebase ID token
   - 参数：
     - `id_token: str` - 客户端 Firebase ID token
   - 返回：解码后的 token 信息
   - 异常：ValueError - token 无效

2. **create_user(email: str, password: str, display_name: Optional[str] = None) -> Dict**
   - 创建新用户
   - 参数：
     - `email: str` - 用户邮箱
     - `password: str` - 用户密码
     - `display_name: Optional[str]` - 显示名称
   - 返回：用户信息字典
   - 异常：ValueError - 创建失败

3. **get_user(uid: str) -> Dict**
   - 获取用户信息
   - 参数：
     - `uid: str` - 用户唯一标识符
   - 返回：用户信息字典

4. **update_user_data(uid: str, data: Dict) -> Dict**
   - 更新用户数据到 Realtime Database
   - 参数：
     - `uid: str` - 用户唯一标识符
     - `data: Dict` - 要更新的数据
   - 返回：更新后的数据

5. **get_user_data(uid: str) -> Optional[Dict]**
   - 从 Realtime Database 获取用户数据
   - 参数：
     - `uid: str` - 用户唯一标识符
   - 返回：用户数据或 None

6. **save_travel_plan(user_id: str, plan_data: Dict) -> str**
   - 保存旅行计划
   - 参数：
     - `user_id: str` - 用户ID
     - `plan_data: Dict` - 旅行计划数据
   - 返回：计划ID

7. **get_travel_plans(user_id: str) -> List[Dict]**
   - 获取用户的所有旅行计划
   - 参数：
     - `user_id: str` - 用户ID
   - 返回：旅行计划列表

8. **get_travel_plan(user_id: str, plan_id: str) -> Optional[Dict]**
   - 获取特定旅行计划
   - 参数：
     - `user_id: str` - 用户ID
     - `plan_id: str` - 计划ID
   - 返回：旅行计划数据或 None

9. **update_travel_plan(user_id: str, plan_id: str, data: Dict) -> Dict**
   - 更新旅行计划
   - 参数：
     - `user_id: str` - 用户ID
     - `plan_id: str` - 计划ID
     - `data: Dict` - 要更新的数据
   - 返回：更新后的数据

10. **delete_travel_plan(user_id: str, plan_id: str) -> bool**
    - 删除旅行计划
    - 参数：
      - `user_id: str` - 用户ID
      - `plan_id: str` - 计划ID
    - 返回：是否成功

### `ai_service.py`
AI 服务，协调 CrewAI agents 执行任务。

#### 类定义（Classes）

**AIService**
- AI 服务类

#### 静态方法（Static Methods）

1. **generate_travel_plan(request: TravelPlanRequest) -> Dict**
   - 生成旅行计划
   - 参数：
     - `request: TravelPlanRequest` - 旅行计划请求对象
   - 返回：包含计划详情和原始输出的字典
     ```python
     {
         'success': bool,
         'parsed_result': dict,  # 解析后的结果
         'raw_output': str,      # AI 原始输出
         'error': str            # 错误信息（如果失败）
     }
     ```

2. **_parse_crew_output(result) -> Dict**
   - 解析 CrewAI 输出
   - 参数：
     - `result` - CrewAI 执行结果
   - 返回：解析后的结构化数据

## 使用示例

```python
from app.services import FirebaseService, AIService
from app.models import TravelPlanRequest

# Firebase 服务
token = "firebase_id_token"
decoded = FirebaseService.verify_token(token)

# AI 服务
request = TravelPlanRequest(
    from_location="北京",
    destination="成都",
    num_people=2,
    duration=5
)
result = AIService.generate_travel_plan(request)
```

