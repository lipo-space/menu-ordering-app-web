from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class DishBase(BaseModel):
    """Base dish model"""

    name: str = Field(..., min_length=1, max_length=100, description="Dish name")
    description: Optional[str] = Field(None, max_length=500, description="Dish description")


class DishCreate(DishBase):
    """Dish creation model"""

    pass


class DishUpdate(BaseModel):
    """Dish update model"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class Dish(DishBase):
    """Dish model with all fields"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    times_paired: int = Field(default=0, ge=0, description="Times used in combinations")
    times_enjoyed: int = Field(default=0, ge=0, description="Times used in menus")
    created_at: datetime
    updated_at: datetime


class DishList(BaseModel):
    """Dish list response model"""

    data: list[Dish]
    meta: dict


# For temporary demo without database
class TempDish(BaseModel):
    """Temporary dish model for demo"""

    id: str
    name: str
    description: Optional[str] = None
    times_paired: int = 0
    times_enjoyed: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
