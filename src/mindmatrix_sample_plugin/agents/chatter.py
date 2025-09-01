from typing import List, Callable

from mindmatrix import MindMatrix, BaseAgent, OpenAILike


# 智能体的角色
CHATTER_DESCRIPTION = """
你是一个智能协作助手，名字叫做Chatter，是用户请求的最终回复者。
"""


# 智能体的目标(任务)
CHATTER_GOAL = """
当用户的请求没有匹配到其他协作者时，你会接收到这个请求，你需要回复用户。
"""


# 智能体的指令（约束）
CHATTER_INSTRUCTIONS = [
    "语言精炼，不要啰嗦", 
    "回答符合人类交流的语气，不能包含表情",
]


def create_chatter(
    mm: MindMatrix,
    model: OpenAILike,
    name: str = "闲聊",
    description: str = None,
    goal: str = None,
    instructions: List[str] = None,
    tools: List[Callable] = None,
    show_tool_calls: bool = False,
    **kwargs
) -> BaseAgent:
    if description is None:
        description = CHATTER_DESCRIPTION
    if goal is None:
        goal = CHATTER_GOAL
    if instructions is None:
        instructions = CHATTER_INSTRUCTIONS
    
    return BaseAgent(
        model=model,
        name=name,
        description=description,
        goal=goal,
        instructions=instructions,
        tools=tools,
        show_tool_calls=show_tool_calls,
        **kwargs
    )
