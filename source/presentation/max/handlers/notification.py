from source.presentation.max.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState, fsm

from typing import Dict


class NotificationsHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return payload == "notifications"

    async def handle(self, update: Dict,user_id: int, chat_id: int):
        _, payload, _ = self._parse_update(update)

        if payload == "notifications":
            setting = await self.repo.get_notifications(chat_id)
            text = f"Новые проблемы: {'Да' if setting.new_problems else 'Нет'}\nСводка: {'Да' if setting.daily_summary else 'Нет'}"
            buttons = [
                [Button(type="callback", text="Перекл. проблемы", payload="toggle_problems")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text=text)
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload == "toggle_problems":
            setting = await self.repo.get_notifications(chat_id)
            await self.repo.update_notifications(chat_id, new_problems=not setting.new_problems)
            body = NewMessageBody(text="Обновлено!")
            await self.client.send_message(chat_id, body)
            return

        body = NewMessageBody(text="Не понял. Вернитесь к уведомлениям.")
        buttons = [[Button(type="callback", text="🔔 Уведомления", payload="notifications")]]
        await self.client.send_message(chat_id, body, buttons)