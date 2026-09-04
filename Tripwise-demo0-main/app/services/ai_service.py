"""
AI服务模块
AI Service Module

负责协调CrewAI agents执行旅行规划任务。
Coordinates CrewAI agents to execute travel planning tasks.

Functions:
    - generate_travel_plan(request): 生成旅行计划
    - parse_agent_output(output): 解析AI输出
"""

from crewai import Crew, Process
from typing import Dict
from app.models.travel_plan import TravelPlanRequest
from app.agents.planner_agent import create_planner, create_planning_task
from app.agents.writer_agent import create_writer, create_itinerary_task
from app.config import Config


class AIService:
    """
    AI服务类
    AI Service Class
    
    使用CrewAI agents生成旅行计划。
    Uses CrewAI agents to generate travel plans.
    """
    
    @staticmethod
    def generate_travel_plan(request: TravelPlanRequest) -> Dict:
        """
        生成旅行计划
        Generate Travel Plan
        
        Args:
            request: 旅行计划请求对象
            
        Returns:
            Dict: 包含计划详情和原始输出的字典
        """
        try:
            # 创建agents
            planner = create_planner(
                request.from_location,
                request.destination,
                request.num_people
            )
            writer = create_writer(
                request.from_location,
                request.destination
            )
            
            # 创建tasks
            planning_task = create_planning_task(
                planner,
                request.from_location,
                request.destination,
                request.num_people,
                request.duration
            )
            itinerary_task = create_itinerary_task(
                writer,
                request.from_location,
                request.destination,
                request.duration
            )
            
            # 执行Crew
            crew = Crew(
                agents=[planner, writer],
                tasks=[planning_task, itinerary_task],
                verbose=True,
                process=Process.sequential
            )
            
            result = crew.kickoff()
            
            # 解析结果
            parsed_result = AIService._parse_crew_output(result)
            
            return {
                'success': True,
                'parsed_result': parsed_result,
                'raw_output': str(result)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'raw_output': None
            }
    
    @staticmethod
    def _parse_crew_output(result) -> Dict:
        """
        解析CrewAI输出
        Parse CrewAI Output
        
        Args:
            result: CrewAI执行结果
            
        Returns:
            Dict: 解析后的结构化数据
        """
        try:
            parsed = {
                'planning_result': '',
                'itinerary_result': '',
                'tasks': []
            }
            
            # 尝试从result.tasks获取任务输出
            if hasattr(result, 'tasks') and result.tasks:
                if len(result.tasks) > 0:
                    parsed['planning_result'] = str(result.tasks[0].output)
                if len(result.tasks) > 1:
                    parsed['itinerary_result'] = str(result.tasks[1].output)
                
                parsed['tasks'] = [
                    {
                        'description': task.description,
                        'output': str(task.output) if hasattr(task, 'output') else ''
                    }
                    for task in result.tasks
                ]
            else:
                # Fallback: 使用完整输出
                parsed['planning_result'] = str(result)
                parsed['itinerary_result'] = str(result)
            
            return parsed
            
        except Exception as e:
            # 如果解析失败，返回原始字符串
            return {
                'planning_result': str(result),
                'itinerary_result': '',
                'parse_error': str(e)
            }

