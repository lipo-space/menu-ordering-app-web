from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from .dish import Dish


class CombinationBase(BaseModel):
    name: str


class CombinationCreate(CombinationBase):
    dish_ids: List[UUID]


class CombinationUpdate(BaseModel):
    name: Optional[str] = None
    dish_ids: Optional[List[UUID]] = None


class Combination(CombinationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dishes: List[Dish] = Field(default_factory=list)
    created_at: datetime


class CombinationList(BaseModel):
    data: List[Combination]
    meta: dict
