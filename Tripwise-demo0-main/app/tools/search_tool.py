"""
互联网搜索工具
Internet Search Tool

提供基于Serper API的互联网搜索功能。
Provides internet search functionality using Serper API.

Classes:
    - SearchInternetToolSchema: 搜索工具参数Schema
    - SearchInternetTool: 搜索工具实现
    
Functions:
    - search_with_serper(query, n_results): 使用Serper API执行搜索
"""

import json
import requests
from typing import List, Dict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from app.config import Config


class SearchInternetToolSchema(BaseModel):
    """
    搜索工具参数Schema
    Search Tool Arguments Schema
    """
    query: str = Field(..., description="The search query for the internet.")


class SearchInternetTool(BaseTool):
    """
    互联网搜索工具
    Internet Search Tool
    
    使用Serper API进行互联网搜索。
    Performs internet searches using Serper API.
    
    Attributes:
        name: 工具名称
        description: 工具描述
        args_schema: 参数Schema
    """
    
    name: str = "Search internet"
    description: str = (
        "Search the internet for a given topic and return relevant results. "
        "Useful for finding current information about flights, hotels, "
        "attractions, and travel-related topics."
    )
    args_schema: type = SearchInternetToolSchema

    def _run(self, query: str) -> List[Dict[str, str]]:
        """
        执行搜索
        Execute Search
        
        Args:
            query: 搜索查询字符串
            
        Returns:
            List[Dict]: 搜索结果列表
        """
        print(f"🔍 [Search Tool] Searching for: {query}")
        return search_with_serper(query)


def search_with_serper(query: str, n_results: int = 5) -> List[Dict[str, str]]:
    """
    使用Serper API执行搜索
    Perform Search Using Serper API
    
    Args:
        query: 搜索查询字符串
        n_results: 返回结果数量
        
    Returns:
        List[Dict]: 搜索结果列表
        [
            {
                'title': '标题',
                'link': '链接',
                'snippet': '摘要'
            },
            ...
        ]
    """
    api_key = Config.API_KEYS.get('serper')
    
    if not api_key:
        print("⚠️  Warning: Serper API key not configured")
        return [{
            "error": "Serper API key not configured",
            "message": "Please set SERPER_API_KEY in environment variables"
        }]
    
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': api_key,
        'content-type': 'application/json',
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        results = response.json().get('organic', [])
        
        formatted_results = []
        for result in results[:n_results]:
            formatted_results.append({
                "title": result.get("title", "No Title Available"),
                "link": result.get("link", "No Link Available"),
                "snippet": result.get("snippet", "No Snippet Available")
            })
        
        print(f"✅ [Search Tool] Found {len(formatted_results)} results")
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        print(f"❌ [Search Tool] Error: {e}")
        return [{"error": f"Error during search: {e}"}]

