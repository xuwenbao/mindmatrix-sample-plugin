# MindMatrix Sample Plugin

> 此项目展示了如何为 MindMatrix 创建一个示例插件。

## 项目概述

MindMatrix Sample Plugin 是一个完整的 MindMatrix 插件示例，展示了如何创建、配置和部署一个自定义智能体插件。该插件包含一个名为 "Chatter" 的智能体，可以作为用户请求的最终回复者。

## 项目结构

```
mindmatrix-sample-plugin/
├── src/
│   └── mindmatrix_sample_plugin/
│       ├── __init__.py              # 插件入口点
│       ├── __about__.py             # 版本信息
│       ├── _plugin.py               # 插件注册逻辑
│       ├── settings.py              # 配置管理
│       └── agents/
│           ├── __init__.py
│           └── chatter.py           # Chatter 智能体实现
├── scripts/
│   └── server.py                    # 服务器启动脚本
├── pyproject.toml                   # 项目配置和依赖
└── README.md                        # 项目文档
```

## 核心组件

### 1. 插件注册 (`_plugin.py`)

插件通过 `register_plugin` 函数向 MindMatrix 注册智能体：

```python
def register_plugin(mm: MindMatrix, **kwargs):
    settings = get_settings()
    
    # 注册智能体工厂
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
```

### 2. 智能体实现 (`agents/chatter.py`)

Chatter 智能体是一个基于 `BaseAgent` 的简单聊天助手：

- **角色**: 智能协作助手，作为用户请求的最终回复者
- **目标**: 当用户请求没有匹配到其他协作者时，接收并回复用户
- **指令**: 语言精炼，回答符合人类交流语气，不包含表情

### 3. 配置管理 (`settings.py`)

支持多种配置方式：

- **环境变量**: 使用 `MSP_` 前缀
- **配置文件**: 支持 YAML 格式，按优先级从多个位置读取
- **默认配置**: 内置合理的默认值

配置项包括：
- `testing`: 调试模式开关
- `llm.model_id`: 大语言模型 ID
- `llm.base_url`: API 基础 URL
- `llm.api_key`: API 密钥

## 安装和使用

### 1. 安装依赖

```bash
# 使用 uv 安装（推荐）
uv sync

# 或使用 pip 安装
pip install -e .
```

### 2. 配置设置环境变量：

```bash
export MSP_LLM__API_KEY="your-api-key-here"
export MSP_LLM__MODEL_ID="gpt-4o-mini"
export MSP_LLM__BASE_URL="https://api.openai.com"
export MSP_TESTING="true"
```

### 3. 启动服务器

```bash
python scripts/server.py
```

服务器将在 `http://127.0.0.1:9527` 启动。

### 4. 使用 API

启动后，可以通过以下方式与 Chatter 智能体交互：

```bash
# 使用 curl 测试
curl -X POST "http://127.0.0.1:9527/mm/v1/agent/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "chatter",
    "messages": [
      {"role": "user", "content": "你好，请介绍一下自己"}
    ]
  }'
```

## 插件系统

### 入口点配置

在 `pyproject.toml` 中配置插件入口点：

```toml
[project.entry-points."mindmatrix.plugin"]
msp = "mindmatrix_sample_plugin"
```

### 插件接口版本

插件需要声明接口版本以确保兼容性：

```python
__plugin_interface_version__ = 1
```