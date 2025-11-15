from source.presentation.max.handlers.base import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState
from source.core.lexicon.max import FAQ_ITEMS

from typing import Dict

class HelpChoiceHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return payload == "help"

    async def handle(self, update: Dict,user_id: int, chat_id: int):
        _, payload, _ = self._parse_update(update)

        if payload == "help":
            text = "\n\n".join(FAQ_ITEMS)
            body = NewMessageBody(text=text, format="markdown")
            buttons = [[Button(type="callback", text="🔙 Главное меню", payload="main_menu")]]
            await self.client.send_message(chat_id, body, buttons)
            return

        body = NewMessageBody(text="Не понял. Вернитесь к FAQ.")
        buttons = [[Button(type="callback", text="💡 FAQ", payload="help")]]
        await self.client.send_message(chat_id, body, buttons)