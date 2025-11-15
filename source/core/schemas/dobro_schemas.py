from typing import Optional
import datetime

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from source.core.enum.dobro_enum import CategoryType

class Category(BaseModel):
    category_id: CategoryType = Field(..., description="Айди категории")

class Advert(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
   
    image: Optional[str] = Field(..., description="Изображение объявления")
    description: Optional[str] = Field(..., description="Краткое описание")
    title: Optional[str] = Field(..., description="Название объявления")
    id: str = Field(..., description="Айди объявления")
    url: Optional[str] = Field(..., description="Ссылка на объявление")
    goal_amount: Optional[int] = Field(..., description="Цель по пожертвованиям")
    money_collected: Optional[int] = Field(None, description="Собрано средств")
    percent: Optional[int] = Field(None, description="Процент выполнения цели")
    money_left: Optional[int] = Field(None, description="Остаток до цели")
    city_name: Optional[str] = Field(None, description="Город проекта")
    fund_name: Optional[str] = Field(None, description="Название фонда")
    start_date: datetime = Field(None, description="Дата начала")
    end_date: datetime = Field(None, description="Дата окончания")
    is_urgent: Optional[bool] = Field(False, description="Срочный проект")
    lead: Optional[str] = Field(None, description="Подробное описание")
    meta_text: Optional[str] = Field(None, description="Мета-текст")
    has_report: Optional[bool] = Field(False, description="Есть отчет")

class RequestAdvert(BaseModel):
    amount: Optional[int] = Field(..., description="Сумма пожертвования")
    advert_id: Optional[int] = Field(..., description="Айди объявления")

    
