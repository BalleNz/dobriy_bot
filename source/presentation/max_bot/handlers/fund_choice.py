from typing import Dict

from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max_bot.handlers import BaseHandler
from source.presentation.max_bot.states.fsm import UserState, fsm


class FundChoiceHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, text_input = self._parse_update(update)
        # Фикс: уникальные состояния, игнорирует сумму для Donations
        if state in [UserState.FUND_CHOOSING_CATEGORY, UserState.FUND_ENTERING_AMOUNT,
                     UserState.FUND_ENTERING_FREQUENCY]:
            return payload == "fund_choice" or (payload and payload.startswith("fund_cat_")) or (
                        payload and payload.startswith("freq_")) or text_input
        return payload == "fund_choice"

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        state = await fsm.get_state(user_id)
        _, payload, text_input = self._parse_update(update)
        data = fsm.states.get(user_id, {}).get("data", {})
        print(f"DEBUG fund_choice: state = {state}, payload = {payload}, text_input = '{text_input}'")

        if payload == "fund_choice":
            await fsm.set_state(user_id, UserState.FUND_CHOOSING_CATEGORY, data)
            buttons = [
                [Button(type="callback", text="🌍 Экология", payload="fund_cat_ecology")],
                [Button(type="callback", text="🏥 Здоровье", payload="fund_cat_health")],
                [Button(type="callback", text="🎓 Образование", payload="fund_cat_education")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text="Шаг 1/3: Выберите категорию:")
            await self.client.send_message(chat_id, body, buttons)
            return

        if state == UserState.FUND_CHOOSING_CATEGORY and payload and payload.startswith("fund_cat_"):
            data["category"] = payload.split("_")[-1]
            await fsm.set_state(user_id, UserState.FUND_ENTERING_AMOUNT, data)
            body = NewMessageBody(text="Шаг 2/3: Введите сумму (например: 500):")
            await self.client.send_message(chat_id, body)
            return

        if state == UserState.FUND_ENTERING_AMOUNT and text_input:
            try:
                amount = float(text_input.strip())
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной.")
                data["amount"] = amount
                await fsm.set_state(user_id, UserState.FUND_ENTERING_FREQUENCY, data)
                buttons = [
                    [Button(type="callback", text="Единовременно", payload="freq_once")],
                    [Button(type="callback", text="Ежемесячно", payload="freq_monthly")],
                    [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
                ]
                body = NewMessageBody(text="Шаг 3/3: Выберите частоту:")
                await self.client.send_message(chat_id, body, buttons)
                return
            except ValueError:
                body = NewMessageBody(text="Неверная сумма. Введите число (например: 500):")
                await self.client.send_message(chat_id, body)
                return

        if state == UserState.FUND_ENTERING_FREQUENCY and payload and payload.startswith("freq_"):
            data["frequency"] = payload.split("_")[-1]
            await fsm.set_state(user_id, UserState.IDLE, data)

        print(f"DEBUG fund_choice: Fallback for payload={payload}, state={state}")
        body = NewMessageBody(text="Не понял. Вернитесь к выбору фонда.")
        buttons = [[Button(type="callback", text="🏆 Выбор фонда", payload="fund_choice")]]
        await self.client.send_message(chat_id, body, buttons)
