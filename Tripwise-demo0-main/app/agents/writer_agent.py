"""
旅行行程编写Agent
Travel Itinerary Writer Agent

负责将规划信息整理成详细的旅行行程。
Responsible for organizing planning information into detailed travel itineraries.

Functions:
    - create_writer(from_location, destination): 创建编写agent
    - create_itinerary_task(writer, from_location, destination, duration): 创建行程编写任务
"""

from crewai import Agent, Task, LLM
from app.config import Config
from app.tools.search_tool import SearchInternetTool


def create_writer(from_location: str, destination: str) -> Agent:
    """
    创建旅行行程编写专家Agent
    Create Vacation Itinerary Creator Agent
    
    Args:
        from_location: 出发地
        destination: 目的地
        
    Returns:
        Agent: 配置好的编写Agent
    """
    # 获取LLM配置
    llm_config = Config.LLM_CONFIG
    llm = LLM(
        model=llm_config['model'],
        base_url=llm_config['base_url'],
        provider=llm_config['provider']
    )
    
    # 创建搜索工具
    search_tool = SearchInternetTool()
    
    return Agent(
        role='Vacation Itinerary Creator',
        goal=f"Create a detailed vacation itinerary from {from_location} to {destination}.",
        backstory=f"""You are a travel content creator who crafts engaging and informative itineraries.
        Your job is to use the data provided by the Travel Planner to create a clear and 
        structured itinerary for a trip from {from_location} to {destination}.
        
        You excel at:
        - Creating day-by-day schedules
        - Balancing activities and rest time
        - Including practical travel information
        - Providing tips and recommendations
        - Organizing information in an easy-to-read format
        
        You always create itineraries that are:
        - Well-structured and easy to follow
        - Include specific times and locations
        - Consider travel logistics between locations
        - Account for meals and rest periods""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        max_iter=5,
        tools=[search_tool],
    )


def create_itinerary_task(
    writer: Agent,
    from_location: str,
    destination: str,
    duration: int
) -> Task:
    """
    创建行程编写任务
    Create Itinerary Writing Task
    
    Args:
        writer: 编写Agent
        from_location: 出发地
        destination: 目的地
        duration: 旅行天数
        
    Returns:
        Task: 配置好的行程编写任务
    """
    return Task(
        description=f"""Create a detailed {duration}-day vacation itinerary 
        from {from_location} to {destination}.

        Itinerary Requirements:
        1. Provide a day-by-day breakdown of activities
        2. Include specific times for each activity when possible
        3. Account for meal times (breakfast, lunch, dinner)
        4. Include accommodation information for each night
        5. Consider travel time between locations
        6. Add practical tips and recommendations
        7. Include cost information from the planning research
        
        Use the information provided by the Travel Research Specialist to create 
        a comprehensive and practical itinerary.""",
        
        expected_output=f"""A complete {duration}-day vacation itinerary from {from_location} 
        to {destination}, formatted as follows:
        
        **OVERVIEW:**
        - Trip duration: {duration} days
        - Route: {from_location} → {destination}
        - Estimated total cost
        
        **DAY-BY-DAY ITINERARY:**
        
        Day 1: [Date/Title]
        - Morning (9:00 AM): [Activity with location and cost]
        - Lunch (12:00 PM): [Restaurant recommendation]
        - Afternoon (2:00 PM): [Activity with location and cost]
        - Dinner (7:00 PM): [Restaurant recommendation]
        - Accommodation: [Hotel name and address]
        
        [Continue for all {duration} days]
        
        **PRACTICAL INFORMATION:**
        - Transportation details between {from_location} and {destination}
        - Best flight options (with links)
        - Recommended accommodations (with links)
        - Local transportation tips
        - Budget breakdown
        
        **TIPS & RECOMMENDATIONS:**
        - Best time to visit attractions
        - Money-saving tips
        - Cultural considerations
        - Emergency contacts""",
        
        agent=writer,
        max_iter=5
    )

