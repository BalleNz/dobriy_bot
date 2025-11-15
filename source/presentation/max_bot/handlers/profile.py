from typing import Dict

from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max_bot.handlers import BaseHandler
from source.presentation.max_bot.states.fsm import UserState, fsm


class ProfileHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return (
                payload == "profile" or
                payload == "edit_profile" or
                state == UserState.EDITING_PROFILE
        )

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        state = await fsm.get_state(chat_id)
        _, payload, text_input = self._parse_update(update)

        if payload == "profile":
            # profile = await self.repo.get_profile(chat_id)
            text = f"Интересы: {profile.interests if profile else 'Не указаны'}"
            buttons = [
                [Button(type="callback", text="Редактировать", payload="edit_profile")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text=text)
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload == "edit_profile":
            await fsm.set_state(chat_id, UserState.EDITING_PROFILE)
            body = NewMessageBody(text="Введите новые интересы:")
            await self.client.send_message(chat_id, body)
            return

        if state == UserState.EDITING_PROFILE and text_input:
            # await self.repo.update_profile(chat_id, interests=text_input)
            await fsm.clear_state(chat_id)
            body = NewMessageBody(text="Обновлено!")
            buttons = [[Button(type="callback", text="🔙 Профиль", payload="profile")]]
            await self.client.send_message(chat_id, body, buttons)
            return

        body = NewMessageBody(text="Не понял. Вернитесь в профиль.")
        buttons = [[Button(type="callback", text="👤 Профиль", payload="profile")]]
        await self.client.send_message(chat_id, body, buttons)
