"""
旅行规划Agent
Travel Planner Agent

负责研究和规划旅行选项，包括航班、住宿和活动。
Responsible for researching and planning travel options including flights, accommodations, and activities.

Functions:
    - create_planner(from_location, destination, num_people): 创建规划agent
    - create_planning_task(planner, from_location, destination, num_people, duration): 创建规划任务
"""

from crewai import Agent, Task, LLM
from app.config import Config
from app.tools.search_tool import SearchInternetTool


def create_planner(from_location: str, destination: str, num_people: int) -> Agent:
    """
    创建旅行规划专家Agent
    Create Travel Research Specialist Agent
    
    Args:
        from_location: 出发地
        destination: 目的地
        num_people: 旅行人数
        
    Returns:
        Agent: 配置好的规划Agent
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
        role='Travel Research Specialist',
        goal=f'Plan a vacation from {from_location} to {destination} for {num_people} people.',
        backstory=f"""You are an expert travel planner specializing in budget-friendly vacations.
        Your role is to find the best options for travel, accommodation, and activities 
        from {from_location} to {destination}.
        
        You have extensive knowledge of:
        - Flight booking and airline options
        - Hotel and accommodation booking
        - Local attractions and activities
        - Budget optimization strategies
        - Travel logistics and planning
        
        You always provide detailed information with links and costs.""",
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        tools=[search_tool],
        llm=llm,
    )


def create_planning_task(
    planner: Agent,
    from_location: str,
    destination: str,
    num_people: int,
    duration: int
) -> Task:
    """
    创建旅行规划任务
    Create Travel Planning Task
    
    Args:
        planner: 规划Agent
        from_location: 出发地
        destination: 目的地
        num_people: 旅行人数
        duration: 旅行天数
        
    Returns:
        Task: 配置好的规划任务
    """
    return Task(
        description=f"""Find the best vacation options from {from_location} to {destination} 
        for {num_people} people.

        STEPS TO COMPLETE THE TASK:
        1. Search for affordable flights from {from_location} to {destination} and provide 
           at least 3 options with links and costs per person.
        2. Find 4 budget-friendly accommodations in {destination} for {duration} days, 
           with links and total costs.
        3. Identify affordable activities and excursions in {destination} for {num_people} people, 
           with estimated costs per person.
        4. Calculate total estimated costs (flights, accommodation, and activities).
        
        IMPORTANT: Always include actual links to booking websites when available.""",
        
        expected_output=f"""A detailed breakdown of costs for a {destination} vacation 
        for {num_people} people from {from_location}, including:
        
        **FLIGHTS:**
        - 3 flight options with:
          * Airline name
          * Departure and arrival times
          * Cost per person
          * Booking link
        
        **ACCOMMODATIONS:**
        - 4 accommodation options with:
          * Hotel/property name
          * Address
          * Price per night
          * Total cost for {duration} days
          * Booking link
        
        **ACTIVITIES:**
        - List of recommended activities with:
          * Activity name
          * Description
          * Cost per person
          * Total cost for {num_people} people
        
        **TOTAL COST BREAKDOWN:**
        - Flights total: [amount]
        - Accommodation total: [amount]
        - Activities total: [amount]
        - Grand total: [amount]""",
        
        agent=planner,
        max_iter=5
    )

