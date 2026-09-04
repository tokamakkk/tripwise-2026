"""
携程旅行API服务
Ctrip (Trip.com) API Service

集成携程旅行API，提供酒店、机票、景点等旅游产品查询功能。
Integrates Ctrip API for hotels, flights, attractions, and other travel products.

注意：携程API需要企业认证，此处提供基本框架。
Note: Ctrip API requires enterprise certification. This provides a basic framework.

Functions:
    - search_hotels(city, check_in, check_out, guests): 搜索酒店
    - search_flights(from_city, to_city, date, passengers): 搜索航班
    - search_attractions(city): 搜索景点
    - get_hotel_details(hotel_id): 获取酒店详情
"""

import requests
import hashlib
import time
from typing import Dict, List, Optional
from app.config import Config


class CtripService:
    """
    携程旅行服务类
    Ctrip Service Class
    
    提供携程API的封装方法。
    Provides wrapper methods for Ctrip API.
    """
    
    # 携程API基础URL（需要根据实际API更新）
    BASE_URL = "https://openapi.ctrip.com"
    
    def __init__(self):
        """初始化携程服务"""
        self.api_key = Config.API_KEYS.get('ctrip', {}).get('key')
        self.api_secret = Config.API_KEYS.get('ctrip', {}).get('secret')
        
        if not self.api_key or not self.api_secret:
            print("⚠️  Warning: Ctrip API credentials not configured")
    
    def _generate_signature(self, params: Dict) -> str:
        """
        生成API签名
        Generate API Signature
        
        Args:
            params: 请求参数
            
        Returns:
            str: 签名字符串
        """
        # 示例签名生成逻辑（需根据携程实际要求调整）
        sorted_params = sorted(params.items())
        sign_string = ''.join([f"{k}{v}" for k, v in sorted_params])
        sign_string = self.api_secret + sign_string + self.api_secret
        
        return hashlib.md5(sign_string.encode()).hexdigest().upper()
    
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        发起API请求
        Make API Request
        
        Args:
            endpoint: API端点
            params: 请求参数
            
        Returns:
            Dict: API响应数据
        """
        if not self.api_key or not self.api_secret:
            return None
        
        # 添加公共参数
        params['apiKey'] = self.api_key
        params['timestamp'] = str(int(time.time()))
        params['signature'] = self._generate_signature(params)
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.post(url, json=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Ctrip API error: {e}")
            return None
    
    def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str,
        guests: int = 2,
        limit: int = 10
    ) -> List[Dict]:
        """
        搜索酒店
        Search Hotels
        
        Args:
            city: 城市名称
            check_in: 入住日期 (YYYY-MM-DD)
            check_out: 退房日期 (YYYY-MM-DD)
            guests: 入住人数
            limit: 返回结果数量
            
        Returns:
            List[Dict]: 酒店列表
            [
                {
                    'hotel_id': '酒店ID',
                    'name': '酒店名称',
                    'address': '地址',
                    'rating': 评分,
                    'price': 价格,
                    'images': [图片URL],
                    'amenities': [设施列表]
                }
            ]
        """
        params = {
            'city': city,
            'checkIn': check_in,
            'checkOut': check_out,
            'guests': guests,
            'limit': limit,
        }
        
        result = self._make_request('hotel/search', params)
        
        # 解析并返回酒店列表
        if result and result.get('success'):
            return result.get('hotels', [])
        return []
    
    def search_flights(
        self,
        from_city: str,
        to_city: str,
        departure_date: str,
        passengers: int = 1,
        cabin_class: str = 'economy'
    ) -> List[Dict]:
        """
        搜索航班
        Search Flights
        
        Args:
            from_city: 出发城市
            to_city: 到达城市
            departure_date: 出发日期 (YYYY-MM-DD)
            passengers: 乘客人数
            cabin_class: 舱位等级 (economy/business/first)
            
        Returns:
            List[Dict]: 航班列表
            [
                {
                    'flight_number': '航班号',
                    'airline': '航空公司',
                    'departure_time': '起飞时间',
                    'arrival_time': '到达时间',
                    'price': 价格,
                    'duration': '飞行时长',
                    'stops': 中转次数
                }
            ]
        """
        params = {
            'fromCity': from_city,
            'toCity': to_city,
            'departureDate': departure_date,
            'passengers': passengers,
            'cabinClass': cabin_class,
        }
        
        result = self._make_request('flight/search', params)
        
        if result and result.get('success'):
            return result.get('flights', [])
        return []
    
    def search_attractions(self, city: str, limit: int = 20) -> List[Dict]:
        """
        搜索景点
        Search Attractions
        
        Args:
            city: 城市名称
            limit: 返回结果数量
            
        Returns:
            List[Dict]: 景点列表
            [
                {
                    'attraction_id': '景点ID',
                    'name': '景点名称',
                    'description': '描述',
                    'address': '地址',
                    'rating': 评分,
                    'ticket_price': 门票价格,
                    'opening_hours': '开放时间',
                    'images': [图片URL]
                }
            ]
        """
        params = {
            'city': city,
            'limit': limit,
        }
        
        result = self._make_request('attraction/search', params)
        
        if result and result.get('success'):
            return result.get('attractions', [])
        return []
    
    def get_hotel_details(self, hotel_id: str) -> Optional[Dict]:
        """
        获取酒店详情
        Get Hotel Details
        
        Args:
            hotel_id: 酒店ID
            
        Returns:
            Dict: 酒店详细信息
        """
        params = {
            'hotelId': hotel_id,
        }
        
        result = self._make_request('hotel/detail', params)
        
        if result and result.get('success'):
            return result.get('hotel')
        return None
    
    def get_flight_details(self, flight_number: str, date: str) -> Optional[Dict]:
        """
        获取航班详情
        Get Flight Details
        
        Args:
            flight_number: 航班号
            date: 日期 (YYYY-MM-DD)
            
        Returns:
            Dict: 航班详细信息
        """
        params = {
            'flightNumber': flight_number,
            'date': date,
        }
        
        result = self._make_request('flight/detail', params)
        
        if result and result.get('success'):
            return result.get('flight')
        return None

