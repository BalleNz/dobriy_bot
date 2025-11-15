from source.presentation.max.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState, fsm

from typing import Dict


class PrivacyHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return payload == "privacy"

    async def handle(self, update: Dict,user_id: int, chat_id: int):
        _, payload, _ = self._parse_update(update)

        if payload == "privacy":
            profile = await self.repo.get_profile(chat_id)
            share = "Да" if profile.privacy_share_profile else "Нет"
            text = f"Поделиться профилем: {share}"
            buttons = [
                [Button(type="callback", text="Переключить", payload="toggle_share")],
                [Button(type="callback", text="Удалить данные", payload="delete_data")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text=text)
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload == "toggle_share":
            profile = await self.repo.get_profile(chat_id)
            new_share = not profile.privacy_share_profile
            await self.repo.update_profile(chat_id, privacy_share_profile=new_share)
            body = NewMessageBody(text="Обновлено!")
            await self.client.send_message(chat_id, body)
            return

        body = NewMessageBody(text="Не понял. Вернитесь к приватности.")
        buttons = [[Button(type="callback", text="🔒 Приватность", payload="privacy")]]
        await self.client.send_message(chat_id, body, buttons)