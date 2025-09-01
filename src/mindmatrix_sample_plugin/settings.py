import platform
from pathlib import Path
from functools import lru_cache

import yaml
from loguru import logger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


THIS_DIR = Path(__file__).parent
ENV_FILE = Path(THIS_DIR, "../../.env")
CONFIG_FILES = [
    Path("C:\\config.yml") if platform.system() == "Windows" else Path("~/.config.yml").expanduser(),
    Path(THIS_DIR, "../config.yml"),
    Path(THIS_DIR, "../config/config.yml"),
]


class LLMConfig(BaseModel):
    model_id: str = Field(default="gpt-4o-mini", required=True)
    base_url: str = Field(default="https://api.openai.com", required=True)
    api_key: str = Field(required=True)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MSP_', env_file=ENV_FILE.resolve(),
                                      env_nested_delimiter='__') # 以双下划线作为嵌套分隔符
    
    testing: bool = Field(default=False)
    llm: LLMConfig = Field(default_factory=LLMConfig, required=True)

    @staticmethod
    def load() -> "AppSettings":
        # 依次从配置文件列表中，按优先级读取配置文件。
        # 如果未找到配置文件，则返回默认配置。
        for path in CONFIG_FILES:
            if not path.is_file():
                logger.debug(f"未发现配置文件在：`{path.resolve()}`")
                continue

            logger.info(f"读取配置文件从： `{path.resolve()}`")
            with open(path, "r", encoding='utf8') as yaml_file:
                config_data = yaml.safe_load(yaml_file)
                s = AppSettings(**config_data)
                return s
        else:
            return AppSettings()


@lru_cache()
def get_settings() -> AppSettings:
    settings = AppSettings.load()

    if ENV_FILE.exists():
        logger.debug(f'env_file: {ENV_FILE.resolve()}')

    logger.info(f'============================================================')
    logger.info(f'settings: ')
    logger.info(f'testing: {settings.testing}')

    logger.info(f'llm model_id: {settings.llm.model_id}')
    logger.info(f'llm base_url: {settings.llm.base_url}')
    logger.info(f'============================================================')

    return settings
