"""
第三方API服务模块
Third-party API Services Module

集成各种第三方API服务，如高德地图、携程旅行等。
Integrates various third-party API services.
"""

from app.services.third_party.amap_service import AmapService
from app.services.third_party.ctrip_service import CtripService

__all__ = ['AmapService', 'CtripService']

