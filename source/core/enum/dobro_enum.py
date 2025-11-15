from enum import Enum


class CategoryType(str, Enum):
    """
    Категории объявлений на сайте Добро VK
    """
    
    CHILDREN = "KIDS"
    ADULT = "ADULTS"
    ELDERLY = "ELDERLY"
    ANIMALS = "ANIMALS"
    NATURE = "NATURE"
    CULTURE = "CULTURE"
