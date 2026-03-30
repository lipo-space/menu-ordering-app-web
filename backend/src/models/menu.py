from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone
from datetime import date as DateType
from uuid import UUID
from .dish import Dish


class MenuBase(BaseModel):
    """Base menu model"""

    date: DateType = Field(..., description="Menu date")


class MenuCreate(MenuBase):
    """Menu creation model"""

    dish_ids: List[UUID] = Field(..., min_length=1, description="List of dish IDs")


class MenuUpdate(BaseModel):
    """Menu update model"""

    dish_ids: List[UUID] = Field(..., min_length=1, description="List of dish IDs")


class Menu(MenuBase):
    """Menu model with all fields"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dishes: List[Dish] = Field(default_factory=list)
    created_at: datetime


class MenuWithDishes(Menu):
    """Menu with full dish details"""

    dishes: List[Dish] = Field(default_factory=list)


class MenuList(BaseModel):
    """Menu list response model"""

    data: List[MenuWithDishes]
    meta: dict


# For temporary demo without database
class TempMenu(BaseModel):
    """Temporary menu model for demo"""

    id: str
    date: DateType
    dishes: List[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
