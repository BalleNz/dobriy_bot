from source.presentation.max.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState, fsm
from source.core.lexicon.max import STATS_MONTHLY
from typing import Dict

class ResultsHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return payload in ["results", "results_detail"]

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        _, payload, _ = self._parse_update(update)

        if payload == "results":
            body = NewMessageBody(text=STATS_MONTHLY)
            buttons = [
                [Button(type="callback", text="📈 Детали", payload="results_detail")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload == "results_detail":
            detail_text = "Подробная статистика: +20% к сборам за квартал. Помогли 150 семьям."
            body = NewMessageBody(text=detail_text)
            buttons = [[Button(type="callback", text="🔙 Результаты", payload="results")]]
            await self.client.send_message(chat_id, body, buttons)
            return

        body = NewMessageBody(text="Не понял. Вернитесь к результатам.")
        buttons = [[Button(type="callback", text="📊 Результаты", payload="results")]]
        await self.client.send_message(chat_id, body, buttons)