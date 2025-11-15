from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from source.core.enum.dobro_enum import CategoryType


class Category(BaseModel):
    category_id: CategoryType = Field(..., description="Айди категории")


class Advert(BaseModel):
    image: Optional[str] = Field(..., description="Изображение объявления")
    description: Optional[str] = Field(..., description="Краткое описание")
    title: Optional[str] = Field(..., description="Название объявления")
    id: UUID = Field(..., description="Айди объявления")
    url: Optional[str] = Field(..., description="Ссылка на объявление")
    goal_amount: Optional[int] = Field(..., description="Цель по пожертвованиям")


class RequestAdvert(BaseModel):
    amount: Optional[int] = Field(..., description="Сумма пожертвования")
    advert_id: Optional[int] = Field(..., description="Айди объявления")
