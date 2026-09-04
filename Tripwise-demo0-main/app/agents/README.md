# Agents 模块

CrewAI agents 定义和管理模块。

## 文件说明

### `__init__.py`
模块初始化文件，导出 agent 创建函数。

### `planner_agent.py`
旅行规划 Agent。

#### 函数定义（Functions）

1. **create_planner(from_location: str, destination: str, num_people: int) -> Agent**
   - 创建旅行规划专家 Agent
   - 职责：研究和规划旅行选项（航班、住宿、活动）
   - 参数：
     - `from_location: str` - 出发地
     - `destination: str` - 目的地
     - `num_people: int` - 旅行人数
   - 返回：配置好的 Agent 实例
   - Agent 特性：
     - 角色：Travel Research Specialist
     - 工具：SearchInternetTool（互联网搜索）
     - 擅长领域：航班预订、酒店预订、景点活动、预算优化

2. **create_planning_task(planner: Agent, from_location: str, destination: str, num_people: int, duration: int) -> Task**
   - 创建旅行规划任务
   - 参数：
     - `planner: Agent` - 规划 Agent 实例
     - `from_location: str` - 出发地
     - `destination: str` - 目的地
     - `num_people: int` - 旅行人数
     - `duration: int` - 旅行天数
   - 返回：配置好的 Task 实例
   - 任务内容：
     1. 搜索至少 3 个航班选项（含链接和价格）
     2. 找到 4 个经济型住宿选项（含价格和链接）
     3. 推荐活动和景点（含价格）
     4. 计算总费用估算

### `writer_agent.py`
旅行行程编写 Agent。

#### 函数定义（Functions）

1. **create_writer(from_location: str, destination: str) -> Agent**
   - 创建旅行行程编写专家 Agent
   - 职责：将规划信息整理成详细的旅行行程
   - 参数：
     - `from_location: str` - 出发地
     - `destination: str` - 目的地
   - 返回：配置好的 Agent 实例
   - Agent 特性：
     - 角色：Vacation Itinerary Creator
     - 工具：SearchInternetTool
     - 擅长领域：创建日程、平衡活动与休息、提供实用信息

2. **create_itinerary_task(writer: Agent, from_location: str, destination: str, duration: int) -> Task**
   - 创建行程编写任务
   - 参数：
     - `writer: Agent` - 编写 Agent 实例
     - `from_location: str` - 出发地
     - `destination: str` - 目的地
     - `duration: int` - 旅行天数
   - 返回：配置好的 Task 实例
   - 任务内容：
     1. 提供逐日活动明细
     2. 包含具体时间和地点
     3. 考虑用餐时间
     4. 包含住宿信息
     5. 考虑交通时间
     6. 提供实用建议

## Agent 协作流程

```
TravelPlanRequest
    ↓
Planner Agent (研究和规划)
    ↓ 输出：航班、住宿、活动选项
    ↓
Writer Agent (编写行程)
    ↓ 输出：完整的逐日行程
    ↓
TravelPlan (完整计划)
```

## 使用示例

```python
from app.agents import (
    create_planner, 
    create_planning_task,
    create_writer, 
    create_itinerary_task
)
from crewai import Crew, Process

# 创建 agents
planner = create_planner("北京", "成都", 2)
writer = create_writer("北京", "成都")

# 创建 tasks
planning_task = create_planning_task(planner, "北京", "成都", 2, 5)
itinerary_task = create_itinerary_task(writer, "北京", "成都", 5)

# 执行 Crew
crew = Crew(
    agents=[planner, writer],
    tasks=[planning_task, itinerary_task],
    process=Process.sequential
)

result = crew.kickoff()
```

## 扩展指南

### 添加新的 Agent

1. 创建新文件（如 `budget_agent.py`）
2. 实现 `create_agent()` 和 `create_task()` 函数
3. 在 `__init__.py` 中导出
4. 在 `ai_service.py` 中集成到 Crew 中

### Agent 配置参数

- `role`: Agent 的角色定义
- `goal`: Agent 的目标
- `backstory`: Agent 的背景故事（影响行为）
- `verbose`: 是否输出详细日志
- `allow_delegation`: 是否允许委派任务
- `max_iter`: 最大迭代次数
- `tools`: Agent 可用的工具列表
- `llm`: 使用的语言模型

### 性能优化建议

1. 合理设置 `max_iter` 避免过度迭代
2. 为 Agent 提供清晰的 `expected_output` 格式
3. 在 `backstory` 中明确 Agent 的专长领域
4. 使用适当的工具来增强 Agent 能力

