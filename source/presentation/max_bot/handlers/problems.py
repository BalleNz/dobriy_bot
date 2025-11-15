from typing import Dict

from source.core.lexicon.max import PROBLEMS_CATEGORIES
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max_bot.handlers.base import BaseHandler
from source.presentation.max_bot.states.fsm import UserState


class ProblemsHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return payload == "problems" or (payload and payload.startswith("cat_"))

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        _, payload, _ = self._parse_update(update)

        if payload == "problems":
            buttons = [
                [Button(type="callback", text="🌍 Экология", payload=f"cat_ecology")],
                [Button(type="callback", text="👥 Социал.", payload=f"cat_social")],
                [Button(type="callback", text="🏥 Здоровье", payload=f"cat_health")],
                [Button(type="callback", text="🎓 Образов.", payload=f"cat_education")],
                [Button(type="callback", text="♿ Инвалиды", payload=f"cat_disability")],
                [Button(type="callback", text="🔙 Меню", payload="main_menu")]
            ]
            body = NewMessageBody(text="Выберите категорию:")
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload and payload.startswith("cat_"):
            cat = payload.split("_", 1)[1]
            info = PROBLEMS_CATEGORIES.get(cat, "Информация не найдена.")
            buttons = [[Button(type="callback", text="🔙 Главное меню", payload="main_menu")]]
            body = NewMessageBody(text=info)
            await self.client.send_message(chat_id, body, buttons)
            return

        body = NewMessageBody(text="Не понял. Выберите категорию.")
        buttons = [[Button(type="callback", text="🌍 Проблемы", payload="problems")]]
        await self.client.send_message(chat_id, body, buttons)
