from source.infrastructure.max.api_client import Button

MAIN_MENU_BUTTONS = [
    [Button(type="callback", text="🌍 Узнать о проблемах", payload="problems")],
    [Button(type="callback", text="📊 Увидеть реальные результаты", payload="results")],
    [Button(type="callback", text="💡 Помощь без сомнений", payload="help")],
    [Button(type="callback", text="🏆 ПОМОЩЬ В ВЫБОРЕ ФОНДА", payload="fund_choice")],
    [Button(type="callback", text="🔔 Уведомления", payload="notifications")],
    [Button(type="callback", text="👤 Профиль", payload="profile")],
    [Button(type="callback", text="🔒 ПРИВАТНОСТЬ И БЕЗОПАСНОСТЬ", payload="privacy")],
    [Button(type="callback", text="❓ ПОДДЕРЖКА", payload="support")],
    [Button(type="callback", text="💰 Пожертвовать", payload="donate")]
]