from source.presentation.max.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState, fsm

from typing import Dict

class SupportHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return payload == "support"

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        _, payload, _ = self._parse_update(update)

        if payload == "support":
            buttons = [
                [Button(type="link", text="Связаться", url="https://max.ru/support")],
                [Button(type="callback", text="FAQ", payload="support_faq")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text="Поддержка бота")
            await self.client.send_message(chat_id, body, buttons)
            return

        body = NewMessageBody(text="Не понял. Вернитесь к поддержке.")
        buttons = [[Button(type="callback", text="❓ Поддержка", payload="support")]]
        await self.client.send_message(chat_id, body, buttons)