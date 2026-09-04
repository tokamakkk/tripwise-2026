"""
高德地图API服务
Amap (Gaode Maps) API Service

集成高德地图API，提供地理位置、路线规划、POI搜索等功能。
Integrates Amap API for geolocation, route planning, and POI search.

API文档: https://lbs.amap.com/api/

Functions:
    - geocode(address): 地理编码，将地址转换为经纬度
    - reverse_geocode(lat, lon): 逆地理编码，将经纬度转换为地址
    - search_poi(keyword, city): 搜索POI（兴趣点）
    - calculate_route(origin, destination, mode): 计算路线
    - get_distance(origin, destination): 获取两地距离
"""

import requests
from typing import Dict, List, Optional, Tuple
from app.config import Config


class AmapService:
    """
    高德地图服务类
    Amap Service Class
    
    提供高德地图API的封装方法。
    Provides wrapper methods for Amap API.
    """
    
    BASE_URL = "https://restapi.amap.com/v3"
    
    def __init__(self):
        """初始化高德地图服务"""
        self.api_key = Config.API_KEYS.get('amap')
        if not self.api_key:
            print("⚠️  Warning: Amap API key not configured")
    
    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Dict]:
        """
        地理编码 - 地址转坐标
        Geocoding - Address to Coordinates
        
        Args:
            address: 地址字符串
            city: 城市名称（可选，用于提高精确度）
            
        Returns:
            Dict: 包含经纬度的字典
            {
                'formatted_address': '完整地址',
                'location': '经度,纬度',
                'lat': 纬度,
                'lon': 经度
            }
        """
        if not self.api_key:
            return None
        
        url = f"{self.BASE_URL}/geocode/geo"
        params = {
            'key': self.api_key,
            'address': address,
        }
        if city:
            params['city'] = city
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1' and data.get('geocodes'):
                geocode = data['geocodes'][0]
                location = geocode.get('location', '').split(',')
                return {
                    'formatted_address': geocode.get('formatted_address'),
                    'location': geocode.get('location'),
                    'lon': float(location[0]) if len(location) > 0 else None,
                    'lat': float(location[1]) if len(location) > 1 else None,
                }
            return None
            
        except Exception as e:
            print(f"❌ Amap geocode error: {e}")
            return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """
        逆地理编码 - 坐标转地址
        Reverse Geocoding - Coordinates to Address
        
        Args:
            lat: 纬度
            lon: 经度
            
        Returns:
            Dict: 地址信息
        """
        if not self.api_key:
            return None
        
        url = f"{self.BASE_URL}/geocode/regeo"
        params = {
            'key': self.api_key,
            'location': f"{lon},{lat}",
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1' and data.get('regeocode'):
                return data['regeocode']
            return None
            
        except Exception as e:
            print(f"❌ Amap reverse geocode error: {e}")
            return None
    
    def search_poi(
        self,
        keyword: str,
        city: Optional[str] = None,
        types: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        搜索POI（兴趣点）
        Search POI (Point of Interest)
        
        Args:
            keyword: 搜索关键词
            city: 城市名称
            types: POI类型编码
            limit: 返回结果数量限制
            
        Returns:
            List[Dict]: POI列表
        """
        if not self.api_key:
            return []
        
        url = f"{self.BASE_URL}/place/text"
        params = {
            'key': self.api_key,
            'keywords': keyword,
            'offset': limit,
        }
        if city:
            params['city'] = city
        if types:
            params['types'] = types
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1' and data.get('pois'):
                return data['pois']
            return []
            
        except Exception as e:
            print(f"❌ Amap POI search error: {e}")
            return []
    
    def calculate_route(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        mode: str = 'driving'
    ) -> Optional[Dict]:
        """
        计算路线
        Calculate Route
        
        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            mode: 出行方式 (driving/walking/transit)
            
        Returns:
            Dict: 路线信息
        """
        if not self.api_key:
            return None
        
        # 根据模式选择API端点
        endpoint_map = {
            'driving': 'direction/driving',
            'walking': 'direction/walking',
            'transit': 'direction/transit/integrated',
        }
        
        url = f"{self.BASE_URL}/{endpoint_map.get(mode, 'direction/driving')}"
        params = {
            'key': self.api_key,
            'origin': f"{origin[0]},{origin[1]}",
            'destination': f"{destination[0]},{destination[1]}",
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1':
                return data.get('route', {})
            return None
            
        except Exception as e:
            print(f"❌ Amap route calculation error: {e}")
            return None
    
    def get_distance(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[float]:
        """
        获取两地直线距离
        Get Straight-line Distance
        
        Args:
            origin: 起点 (lon, lat)
            destination: 终点 (lon, lat)
            
        Returns:
            float: 距离（米）
        """
        if not self.api_key:
            return None
        
        url = f"{self.BASE_URL}/distance"
        params = {
            'key': self.api_key,
            'origins': f"{origin[0]},{origin[1]}",
            'destination': f"{destination[0]},{destination[1]}",
            'type': 1,  # 直线距离
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '1' and data.get('results'):
                return float(data['results'][0].get('distance', 0))
            return None
            
        except Exception as e:
            print(f"❌ Amap distance calculation error: {e}")
            return None

