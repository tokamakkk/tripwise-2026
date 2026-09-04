# Utils 模块

通用工具函数和装饰器模块。

## 文件说明

### `__init__.py`
模块初始化文件，导出常用工具。

### `decorators.py`
装饰器定义。

#### 装饰器（Decorators）

1. **@require_auth**
   - 功能：Firebase 认证装饰器
   - 用途：保护需要认证的路由
   - 行为：
     1. 从 `Authorization` header 提取 Bearer token
     2. 使用 Firebase Admin SDK 验证 token
     3. 将用户信息存储在 `flask.g` 中
     4. 如果验证失败，返回 401 Unauthorized
   - 使用方式：
     ```python
     from app.utils import require_auth
     
     @app.route('/protected')
     @require_auth
     def protected_route():
         user_id = g.user_id
         user_email = g.user_email
         return {'message': 'Authenticated'}
     ```
   - 请求示例：
     ```
     GET /protected HTTP/1.1
     Authorization: Bearer <firebase_id_token>
     ```

2. **@handle_errors**
   - 功能：统一错误处理装饰器
   - 用途：捕获并统一处理异常
   - 行为：
     - `ValueError` → 400 Bad Request
     - `PermissionError` → 403 Forbidden
     - 其他异常 → 500 Internal Server Error
   - 使用方式：
     ```python
     from app.utils import handle_errors
     
     @app.route('/api/endpoint')
     @handle_errors
     def my_route():
         if invalid_data:
             raise ValueError("Invalid data")
         return {'success': True}
     ```

### `validators.py`
数据验证函数。

#### 函数定义（Functions）

1. **validate_travel_request(data: Dict) -> Tuple[bool, str]**
   - 功能：验证旅行请求数据
   - 参数：
     - `data: Dict` - 请求数据字典
   - 返回：
     - `Tuple[bool, str]` - (是否有效, 错误消息)
   - 验证项：
     - 必填字段：`from_location`, `destination`, `num_people`, `duration`
     - 人数范围：1 到 `MAX_TRAVELERS`
     - 天数范围：1 到 `MAX_DURATION_DAYS`
     - 地点非空且不相同
     - 预算为正数（如果提供）
   - 使用示例：
     ```python
     from app.utils import validate_travel_request
     
     data = request.get_json()
     is_valid, error = validate_travel_request(data)
     if not is_valid:
         return jsonify({'error': error}), 400
     ```

2. **validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]**
   - 功能：验证日期范围
   - 参数：
     - `start_date: str` - 开始日期（YYYY-MM-DD）
     - `end_date: str` - 结束日期（YYYY-MM-DD）
   - 返回：
     - `Tuple[bool, str]` - (是否有效, 错误消息)
   - 验证项：
     - 日期格式正确
     - 开始日期早于结束日期
     - 开始日期不在过去
   - 使用示例：
     ```python
     is_valid, error = validate_date_range("2025-11-01", "2025-11-05")
     if not is_valid:
         return jsonify({'error': error}), 400
     ```

3. **validate_email(email: str) -> Tuple[bool, str]**
   - 功能：验证邮箱格式
   - 参数：
     - `email: str` - 邮箱地址
   - 返回：
     - `Tuple[bool, str]` - (是否有效, 错误消息)
   - 验证：使用正则表达式验证邮箱格式
   - 使用示例：
     ```python
     is_valid, error = validate_email("user@example.com")
     if not is_valid:
         return jsonify({'error': error}), 400
     ```

## 使用示例

### 组合使用装饰器和验证器

```python
from flask import Blueprint, request, jsonify, g
from app.utils import require_auth, handle_errors, validate_travel_request

bp = Blueprint('example', __name__)

@bp.route('/create', methods=['POST'])
@require_auth
@handle_errors
def create_something():
    # 认证已通过，用户信息可用
    user_id = g.user_id
    
    # 获取并验证数据
    data = request.get_json()
    is_valid, error = validate_travel_request(data)
    if not is_valid:
        raise ValueError(error)
    
    # 处理业务逻辑
    result = process_data(data, user_id)
    
    return jsonify(result), 201
```

## 配置依赖

### decorators.py
- 依赖：
  - Flask
  - `app.services.firebase_service.FirebaseService`

### validators.py
- 依赖：
  - `app.config.Config`
  - Python 标准库：`datetime`, `re`

## 扩展指南

### 添加新装饰器

1. 在 `decorators.py` 中定义新装饰器：
   ```python
   from functools import wraps
   
   def my_decorator(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           # 装饰器逻辑
           return f(*args, **kwargs)
       return decorated_function
   ```

2. 在 `__init__.py` 中导出：
   ```python
   from app.utils.decorators import my_decorator
   __all__ = [..., 'my_decorator']
   ```

### 添加新验证器

1. 在 `validators.py` 中定义新函数：
   ```python
   def validate_something(data: Any) -> Tuple[bool, str]:
       if not valid:
           return False, "Error message"
       return True, ""
   ```

2. 在 `__init__.py` 中导出

## 常见模式

### 组合多个验证器

```python
def validate_complete_request(data: Dict) -> Tuple[bool, str]:
    # 基本验证
    is_valid, error = validate_travel_request(data)
    if not is_valid:
        return False, error
    
    # 日期验证
    if 'start_date' in data and 'end_date' in data:
        is_valid, error = validate_date_range(
            data['start_date'], 
            data['end_date']
        )
        if not is_valid:
            return False, error
    
    return True, ""
```

### 自定义错误响应

```python
def custom_error_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except CustomException as e:
            return jsonify({
                'error': 'Custom Error',
                'message': str(e),
                'code': e.code
            }), e.status_code
    return decorated_function
```

