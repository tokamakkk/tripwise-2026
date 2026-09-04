# Third-party API Services 模块

第三方 API 集成服务。

## 文件说明

### `__init__.py`
模块初始化文件，导出第三方服务类。

### `amap_service.py`
高德地图 API 服务集成。

#### 类定义（Classes）

**AmapService**
- 高德地图服务类
- 类变量：
  - `BASE_URL: str` - 高德地图 API 基础 URL

#### 实例方法（Instance Methods）

1. **__init__()**
   - 初始化高德地图服务
   - 从配置中读取 API key

2. **geocode(address: str, city: Optional[str] = None) -> Optional[Dict]**
   - 地理编码 - 地址转坐标
   - 参数：
     - `address: str` - 地址字符串
     - `city: Optional[str]` - 城市名称（提高精确度）
   - 返回：包含经纬度的字典
     ```python
     {
         'formatted_address': '完整地址',
         'location': '经度,纬度',
         'lon': float,
         'lat': float
     }
     ```

3. **reverse_geocode(lat: float, lon: float) -> Optional[Dict]**
   - 逆地理编码 - 坐标转地址
   - 参数：
     - `lat: float` - 纬度
     - `lon: float` - 经度
   - 返回：地址信息字典

4. **search_poi(keyword: str, city: Optional[str] = None, types: Optional[str] = None, limit: int = 20) -> List[Dict]**
   - 搜索 POI（兴趣点）
   - 参数：
     - `keyword: str` - 搜索关键词
     - `city: Optional[str]` - 城市名称
     - `types: Optional[str]` - POI 类型编码
     - `limit: int` - 返回结果数量限制
   - 返回：POI 列表

5. **calculate_route(origin: Tuple[float, float], destination: Tuple[float, float], mode: str = 'driving') -> Optional[Dict]**
   - 计算路线
   - 参数：
     - `origin: Tuple[float, float]` - 起点 (lon, lat)
     - `destination: Tuple[float, float]` - 终点 (lon, lat)
     - `mode: str` - 出行方式（driving/walking/transit）
   - 返回：路线信息字典

6. **get_distance(origin: Tuple[float, float], destination: Tuple[float, float]) -> Optional[float]**
   - 获取两地直线距离
   - 参数：
     - `origin: Tuple[float, float]` - 起点 (lon, lat)
     - `destination: Tuple[float, float]` - 终点 (lon, lat)
   - 返回：距离（米）

### `ctrip_service.py`
携程旅行 API 服务集成。

**注意：携程 API 需要企业认证，此处提供基本框架。**

#### 类定义（Classes）

**CtripService**
- 携程旅行服务类
- 类变量：
  - `BASE_URL: str` - 携程 API 基础 URL

#### 实例方法（Instance Methods）

1. **__init__()**
   - 初始化携程服务
   - 从配置中读取 API key 和 secret

2. **_generate_signature(params: Dict) -> str**
   - 生成 API 签名（内部方法）
   - 参数：
     - `params: Dict` - 请求参数
   - 返回：签名字符串

3. **_make_request(endpoint: str, params: Dict) -> Optional[Dict]**
   - 发起 API 请求（内部方法）
   - 参数：
     - `endpoint: str` - API 端点
     - `params: Dict` - 请求参数
   - 返回：API 响应数据

4. **search_hotels(city: str, check_in: str, check_out: str, guests: int = 2, limit: int = 10) -> List[Dict]**
   - 搜索酒店
   - 参数：
     - `city: str` - 城市名称
     - `check_in: str` - 入住日期（YYYY-MM-DD）
     - `check_out: str` - 退房日期（YYYY-MM-DD）
     - `guests: int` - 入住人数
     - `limit: int` - 返回结果数量
   - 返回：酒店列表

5. **search_flights(from_city: str, to_city: str, departure_date: str, passengers: int = 1, cabin_class: str = 'economy') -> List[Dict]**
   - 搜索航班
   - 参数：
     - `from_city: str` - 出发城市
     - `to_city: str` - 到达城市
     - `departure_date: str` - 出发日期（YYYY-MM-DD）
     - `passengers: int` - 乘客人数
     - `cabin_class: str` - 舱位等级（economy/business/first）
   - 返回：航班列表

6. **search_attractions(city: str, limit: int = 20) -> List[Dict]**
   - 搜索景点
   - 参数：
     - `city: str` - 城市名称
     - `limit: int` - 返回结果数量
   - 返回：景点列表

7. **get_hotel_details(hotel_id: str) -> Optional[Dict]**
   - 获取酒店详情
   - 参数：
     - `hotel_id: str` - 酒店ID
   - 返回：酒店详细信息

8. **get_flight_details(flight_number: str, date: str) -> Optional[Dict]**
   - 获取航班详情
   - 参数：
     - `flight_number: str` - 航班号
     - `date: str` - 日期（YYYY-MM-DD）
   - 返回：航班详细信息

## 使用示例

```python
from app.services.third_party import AmapService, CtripService

# 高德地图服务
amap = AmapService()
location = amap.geocode("天安门", city="北京")
pois = amap.search_poi("景点", city="北京")

# 携程服务
ctrip = CtripService()
hotels = ctrip.search_hotels("成都", "2025-11-01", "2025-11-05")
flights = ctrip.search_flights("北京", "成都", "2025-11-01")
```

## 扩展指南

1. 添加新的第三方 API 服务：
   - 在此目录创建新文件（如 `booking_service.py`）
   - 实现服务类，遵循相同的模式
   - 在 `__init__.py` 中导出

2. API 密钥配置：
   - 在 `.env` 文件中添加密钥
   - 在 `app/config.py` 的 `API_KEYS` 字典中配置
   - 在服务类的 `__init__` 中读取

