"""
Base classes for huquqAI system
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Entity(BaseModel):
    """Base entity class"""
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


class Repository(ABC):
    """Base repository interface"""

    @abstractmethod
    async def find_by_id(self, entity_id: str) -> Optional[Any]:
        """Find entity by ID"""
        pass

    @abstractmethod
    async def find_all(self) -> List[Any]:
        """Find all entities"""
        pass

    @abstractmethod
    async def save(self, entity: Any) -> Any:
        """Save entity"""
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        pass


class Service(ABC):
    """Base service interface"""

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Execute service"""
        pass


class QueryResult(BaseModel):
    """Query result model"""
    success: bool
    data: Any
    message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
