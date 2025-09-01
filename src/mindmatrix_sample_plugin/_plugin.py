from mindmatrix import MindMatrix, OpenAILike

from .settings import get_settings
from .agents import (
    create_chatter,
)


__plugin_interface_version__ = (
    1  # The version of the plugin interface that this plugin uses
)


def register_plugin(mm: MindMatrix, **kwargs):
    settings = get_settings()
    
    # register agents
    mm.register_agent_factory(
        agent_name="chatter",
        agent_factory=create_chatter,
        agent_config={
            "name": "chatter",
            "model": OpenAILike(
                id=settings.llm.model_id,
                api_key=settings.llm.api_key,
                base_url=settings.llm.base_url,
            ),
            "debug_mode": settings.testing,
        },
    )
