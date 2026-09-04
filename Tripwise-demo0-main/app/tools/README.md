# Tools 模块

CrewAI agents 使用的工具集合。

## 文件说明

### `__init__.py`
模块初始化文件，导出所有工具类。

### `search_tool.py`
互联网搜索工具。

#### 类定义（Classes）

1. **SearchInternetToolSchema**
   - 搜索工具参数 Schema
   - 继承自：`pydantic.BaseModel`
   - 属性：
     - `query: str` - 搜索查询字符串（必填）

2. **SearchInternetTool**
   - 互联网搜索工具实现
   - 继承自：`crewai.tools.BaseTool`
   - 属性：
     - `name: str` - 工具名称："Search internet"
     - `description: str` - 工具描述
     - `args_schema: type` - 参数 Schema 类
   - 方法：
     - `_run(query: str) -> List[Dict[str, str]]` - 执行搜索

#### 函数定义（Functions）

**search_with_serper(query: str, n_results: int = 5) -> List[Dict[str, str]]**
- 使用 Serper API 执行搜索
- 参数：
  - `query: str` - 搜索查询字符串
  - `n_results: int` - 返回结果数量（默认5）
- 返回：搜索结果列表
  ```python
  [
      {
          'title': '标题',
          'link': '链接',
          'snippet': '摘要'
      },
      ...
  ]
  ```
- 错误处理：如果 API 请求失败，返回错误信息字典

## 使用示例

```python
from app.tools import SearchInternetTool

# 创建搜索工具实例
search_tool = SearchInternetTool()

# 在 Agent 中使用
from crewai import Agent, LLM

agent = Agent(
    role='Researcher',
    goal='Research travel information',
    backstory='Expert researcher',
    tools=[search_tool],  # 添加工具
    llm=llm
)
```

## 配置要求

在 `.env` 文件中配置 Serper API key：
```
SERPER_API_KEY=your_api_key_here
```

获取 API key：https://serper.dev/

## 扩展指南

### 添加新工具

1. 创建新文件（如 `price_comparison_tool.py`）
2. 定义参数 Schema 类（继承 `BaseModel`）
3. 实现工具类（继承 `BaseTool`）：
   ```python
   from crewai.tools import BaseTool
   from pydantic import BaseModel, Field
   
   class MyToolSchema(BaseModel):
       param1: str = Field(..., description="Parameter description")
   
   class MyTool(BaseTool):
       name: str = "My Tool Name"
       description: str = "Tool description for AI"
       args_schema: type = MyToolSchema
       
       def _run(self, param1: str) -> Any:
           # Tool implementation
           return result
   ```
4. 在 `__init__.py` 中导出
5. 在需要的 Agent 中添加到 `tools` 列表

### 可用的工具类型

CrewAI 支持多种工具类型：
- **搜索工具**：互联网搜索、数据库查询
- **API 工具**：调用第三方 API
- **计算工具**：数据处理、计算
- **文件工具**：读写文件
- **自定义工具**：任何 Python 函数

### 工具设计最佳实践

1. **清晰的描述**：在 `description` 中详细说明工具用途
2. **明确的参数**：使用 Pydantic 定义清晰的参数结构
3. **错误处理**：捕获并适当处理异常
4. **日志输出**：使用 print 输出调试信息
5. **返回格式**：保持一致的返回格式，便于 Agent 理解

### 集成第三方 API 工具

可以将 `app/services/third_party/` 中的服务封装为工具：

```python
from app.services.third_party import AmapService
from crewai.tools import BaseTool

class AmapSearchTool(BaseTool):
    name: str = "Search POI with Amap"
    description: str = "Search points of interest using Amap API"
    
    def _run(self, keyword: str, city: str) -> List[Dict]:
        amap = AmapService()
        return amap.search_poi(keyword, city)
```

## 性能考虑

- API 调用添加超时设置（推荐 10-15 秒）
- 实现重试机制处理临时性故障
- 缓存频繁查询的结果
- 限制返回结果数量避免 token 过多

