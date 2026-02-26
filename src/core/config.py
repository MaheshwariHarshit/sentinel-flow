import os
import yaml
from pydantic import BaseModel

class SystemConfig(BaseModel):
    max_iterations: int = 5
    model: str = "gpt-4o"
    temperature: float = 0.2
    log_level: str = "INFO"

class IntegrationConfig(BaseModel):
    index: str = "main"
    index_name: str = "sentinel-flow-memory"
    enabled: bool = True
    channel: str = "#incidents"

class IntegrationsConfig(BaseModel):
    splunk: IntegrationConfig = IntegrationConfig()
    pinecone: IntegrationConfig = IntegrationConfig()
    github: IntegrationConfig = IntegrationConfig()
    slack: IntegrationConfig = IntegrationConfig()

class DatabaseConfig(BaseModel):
    postgres_uri: str
    redis_uri: str

class AppConfig(BaseModel):
    system: SystemConfig
    integrations: IntegrationsConfig
    database: DatabaseConfig

def load_config(path: str = "config.yaml") -> AppConfig:
    with open(path, "r") as f:
        config_dict = yaml.safe_load(f)
    return AppConfig(**config_dict)

# Load globally
config = load_config()
