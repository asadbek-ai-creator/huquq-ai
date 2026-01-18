"""
Configuration loader for huquqAI system
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class LanguageConfig(BaseModel):
    """Language configuration model"""
    default: str = "kaa"
    supported: list[str] = ["kaa", "uz", "ru", "en"]


class OntologyConfig(BaseModel):
    """Ontology configuration model"""
    base_uri: str
    namespaces: Dict[str, str]
    classes: list[str]
    properties: Dict[str, list[str]]


class SPARQLConfig(BaseModel):
    """SPARQL endpoint configuration"""
    endpoint: str
    update_endpoint: str
    graph_store: str
    default_graph: str
    timeout: int = 30
    retry_count: int = 3


class APIConfig(BaseModel):
    """API configuration model"""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    workers: int = 1


class Config(BaseModel):
    """Main configuration model"""
    application: Dict[str, Any]
    language: LanguageConfig
    terminology: Dict[str, Any]
    ontology: OntologyConfig
    sparql: SPARQLConfig
    api: APIConfig
    nlp: Dict[str, Any]
    logging: Dict[str, Any]
    paths: Dict[str, str]
    search: Dict[str, Any]


class ConfigLoader:
    """Configuration loader class"""

    _instance: Optional['ConfigLoader'] = None
    _config: Optional[Config] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self, config_path: str = "config.yaml") -> Config:
        """Load configuration from YAML file"""
        if self._config is not None:
            return self._config

        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)

        self._config = Config(**config_dict)
        return self._config

    @property
    def config(self) -> Config:
        """Get current configuration"""
        if self._config is None:
            self._config = self.load()
        return self._config


# Global config instance
def get_config() -> Config:
    """Get configuration instance"""
    loader = ConfigLoader()
    return loader.config
