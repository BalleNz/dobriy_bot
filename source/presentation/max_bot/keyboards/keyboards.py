from source.infrastructure.max.api_client import Button

from source.infrastructure.max.api_client import Button

MAIN_MENU_BUTTONS = [
    # Ряд 1: Основные действия по контенту
    [
        Button(type="callback", text="🌍 Узнать о проблемах", payload="problems"),
        Button(type="callback", text="📊 Увидеть результаты", payload="results")
    ],
    # Ряд 2: Быстрая помощь и донат
    [
        Button(type="callback", text="💡 Помощь", payload="help"),
        Button(type="callback", text="💰 Пожертвовать", payload="donate")
    ],
    # Ряд 3: Выбор фонда (отдельный ряд для акцента)
    [
        #Button(type="callback", text="🏆 Выбор фонда", payload="fund_choice")
    ],
    # Ряд 4: Настройки пользователя
    [
        #Button(type="callback", text="🔔 Уведомления", payload="notifications"),
        Button(type="callback", text="👤 Профиль", payload="profile")
    ],
    # Ряд 5: Инфо и поддержка 
    [
        #Button(type="callback", text="🔒 Приватность", payload="privacy"),
        Button(type="callback", text="❓ Поддержка", payload="support")
    ]
]