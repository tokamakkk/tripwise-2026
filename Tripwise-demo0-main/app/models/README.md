# Models 模块

数据模型定义模块，使用 Pydantic 进行数据验证。

## 文件说明

### `__init__.py`
模块初始化文件，导出所有模型类。

### `user.py`
用户相关数据模型。

#### 类定义（Classes）

1. **User**
   - 用户主模型
   - 属性：
     - `uid: str` - Firebase 用户唯一标识符
     - `email: EmailStr` - 用户邮箱
     - `display_name: Optional[str]` - 用户显示名称
     - `created_at: str` - 账户创建时间
     - `last_login: Optional[str]` - 最后登录时间
     - `preferences: Optional[dict]` - 用户偏好设置

2. **UserLogin**
   - 用户登录请求模型
   - 属性：
     - `email: EmailStr` - 用户邮箱
     - `password: str` - 用户密码（最小长度6）

3. **UserRegister**
   - 用户注册请求模型
   - 属性：
     - `email: EmailStr` - 用户邮箱
     - `password: str` - 用户密码（最小长度6）
     - `display_name: Optional[str]` - 用户显示名称

4. **UserProfile**
   - 用户资料更新模型
   - 属性：
     - `display_name: Optional[str]` - 用户显示名称
     - `preferences: Optional[dict]` - 用户偏好设置

### `travel_plan.py`
旅行计划相关数据模型。

#### 类定义（Classes）

1. **TravelPlanRequest**
   - 旅行计划请求模型
   - 属性：
     - `from_location: str` - 出发地
     - `destination: str` - 目的地
     - `num_people: int` - 旅行人数（1-10）
     - `duration: int` - 旅行天数（1-30）
     - `budget: Optional[float]` - 预算（CNY）
     - `preferences: Optional[Dict]` - 偏好设置
   - 验证器：
     - `validate_location()` - 验证地点不为空

2. **FlightOption**
   - 航班选项模型
   - 属性：
     - `airline: str` - 航空公司名称
     - `departure_time: str` - 起飞时间
     - `arrival_time: str` - 到达时间
     - `price: float` - 单人价格
     - `link: Optional[str]` - 预订链接

3. **AccommodationOption**
   - 住宿选项模型
   - 属性：
     - `name: str` - 酒店名称
     - `address: str` - 地址
     - `rating: Optional[float]` - 评分（0-5）
     - `price_per_night: float` - 每晚价格
     - `total_price: float` - 总价格
     - `link: Optional[str]` - 预订链接

4. **Activity**
   - 活动/景点模型
   - 属性：
     - `name: str` - 活动名称
     - `description: Optional[str]` - 活动描述
     - `duration: Optional[str]` - 持续时间
     - `price: float` - 单人价格
     - `location: Optional[str]` - 位置

5. **DayItinerary**
   - 每日行程模型
   - 属性：
     - `day: int` - 天数编号
     - `date: Optional[str]` - 日期
     - `activities: List[Activity]` - 活动列表
     - `meals: Optional[Dict]` - 用餐计划
     - `accommodation: Optional[str]` - 住宿信息
     - `notes: Optional[str]` - 备注

6. **TravelPlan**
   - 完整旅行计划模型
   - 属性：
     - `plan_id: Optional[str]` - 计划唯一标识符
     - `user_id: str` - 用户ID
     - `request: TravelPlanRequest` - 原始请求
     - `flights: List[FlightOption]` - 航班选项列表
     - `accommodations: List[AccommodationOption]` - 住宿选项列表
     - `itinerary: List[DayItinerary]` - 每日行程列表
     - `total_cost: Optional[float]` - 总费用估算
     - `created_at: str` - 创建时间
     - `status: str` - 计划状态（pending/processing/completed/failed）
     - `raw_output: Optional[Dict]` - AI原始输出

## 使用示例

```python
from app.models import User, TravelPlanRequest, TravelPlan

# 创建旅行请求
request = TravelPlanRequest(
    from_location="北京",
    destination="成都",
    num_people=2,
    duration=5,
    budget=5000.0
)

# 验证会自动进行
print(request.dict())
```

