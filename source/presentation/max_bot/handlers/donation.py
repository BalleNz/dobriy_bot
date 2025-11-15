from source.presentation.max.handlers.base import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState, fsm 
from source.core.lexicon.max import DONATION_CATEGORIES
from source.presentation.max.keyboards.keyboards import MAIN_MENU_BUTTONS
from source.infrastructure.parser.dobro import DobroApiClient
from source.core.schemas.dobro_schemas import Advert
from source.infrastructure.dishka import make_dishka_container


from typing import Dict, List

from source.core.lexicon.max import DONATION_CATEGORIES
from source.core.schemas.dobro_schemas import Advert
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.infrastructure.parser.dobro import DobroApiClient
from source.presentation.max_bot.handlers.base import BaseHandler
from source.presentation.max_bot.states.fsm import UserState, fsm


class DonationsHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        update_type, payload, text_input = self._parse_update(update)
        if state == UserState.DONATION_ENTERING_AMOUNT and text_input:
            return True
        return (
            payload == "donate" or
            (payload and payload.startswith("donate_cat_")) or
            (payload and payload.startswith("select_advert_")) or
            (payload and payload.startswith("donate_money_")) or
            payload == "donate_money" or
            payload == "main_menu" or
            state in [UserState.DONATING_CATEGORY, UserState.SELECTING_ADVERT, UserState.ENTERED_ADVERT]
        )

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        dishka_container = make_dishka_container()
        client: DobroApiClient = await dishka_container.get(DobroApiClient)
        state = await fsm.get_state(user_id)
        _, payload, text_input = self._parse_update(update)
        data = fsm.states.get(user_id, {}).get("data", {})
        print(
            f"DEBUG donations: state = {state}, payload = {payload}, text_input = '{text_input}', data_keys = {list(data.keys())}")

        if payload == "donate":
            await fsm.set_state(user_id, UserState.DONATING_CATEGORY)
            buttons = [
                [Button(type="callback", text=info["text"], payload=f"donate_cat_{key}")]
                for key, info in DONATION_CATEGORIES.items()
            ]
            buttons.append([Button(type="callback", text="Назад", payload="main_menu")])
            body = NewMessageBody(text="Выберите категорию для пожертвования:")
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload == "main_menu":
            await fsm.clear_state(user_id)
            body = NewMessageBody(text="Главное меню")
            buttons = MAIN_MENU_BUTTONS
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload and payload.startswith("donate_cat_"):
            cat_key = payload.split("_", 2)[-1]
            cat_info = DONATION_CATEGORIES.get(cat_key)
            if not cat_info:
                await self.client.send_message(chat_id, NewMessageBody(text="Категория не найдена."))
                return

            category_enum = cat_info["enum"]
            data["category"] = cat_key
            await fsm.set_state(user_id, UserState.SELECTING_ADVERT, data)

            all_adverts: List[Advert] = await client.get_adverts(recipient=category_enum, max_pages=1, page_size=5)
            data["adverts"] = all_adverts

            if not all_adverts:
                body = NewMessageBody(text=f"В категории '{cat_key}' объявлений пока нет.")
                buttons = [[Button(type="callback", text="Категории", payload="donate")]]
                await self.client.send_message(chat_id, body, buttons)
                return

            for i, advert in enumerate(all_adverts[:5]):
                token = await self.client.upload_image_from_url(advert.image) if advert.image else ''
                attachments = [{"type": "image", "payload": {"token": token}}] if token else []
                
                urgency_text = " 🔥 СРОЧНО" if advert.is_urgent else ""
                progress_text = f"Собрано: {advert.money_collected:,} ₽ ({advert.percent}%) из {advert.goal_amount:,} ₽\nОстаток: {advert.money_left:,} ₽" if advert.money_collected and advert.goal_amount else f"Цель: {advert.goal_amount or 'Не указана'} ₽"
                location_text = f"\nГород: {advert.city_name}" if advert.city_name else ""
                fund_text = f"\nФонд: {advert.fund_name}" if advert.fund_name else ""
                dates_text = ""
                if advert.start_date and advert.end_date:
                    dates_text = f"\nПериод: {advert.start_date.strftime('%d.%m.%Y')} – {advert.end_date.strftime('%d.%m.%Y')}"
                report_text = "\n📊 Есть отчет" if advert.has_report else ""
                
                text = f"**{advert.title or 'Объявление'}{urgency_text}**\n\n{advert.description}\n\n{progress_text}{location_text}{fund_text}{dates_text}{report_text}"
                if advert.meta_text:
                    text += f"\n\n{advert.meta_text}"
                
                buttons = [[Button(type="callback", text="Пожертвовать", payload=f"donate_money_{str(advert.id)}")]]
                body = NewMessageBody(text=text, format="markdown", attachments=attachments)
                await self.client.send_message(chat_id, body, buttons)

            body = NewMessageBody(text="Выберите объявление выше.")
            buttons = [
                [Button(type="callback", text="Категории", payload="donate")],
                [Button(type="callback", text="Главное меню", payload="main_menu")]
            ]
            await self.client.send_message(chat_id, body, buttons)
            return

        if state == UserState.SELECTING_ADVERT and payload and payload.startswith("donate_money_"):
            advert_id = payload.split("_", 2)[-1]
            all_adverts = data.get("adverts", [])
            advert = next((a for a in all_adverts if a.id == advert_id), None)
            if not advert:
                await self.client.send_message(chat_id, NewMessageBody(text="Объявление не найдено."))
                return
            data["selected_advert_id"] = advert.id
            await fsm.set_state(user_id, UserState.DONATION_ENTERING_AMOUNT, data)
        
            urgency_text = " 🔥 СРОЧНО" if advert.is_urgent else ""
            progress_text = f"Собрано: {advert.money_collected:,} ₽ ({advert.percent}%) из {advert.goal_amount:,} ₽" if advert.money_collected and advert.goal_amount else ""
            location_text = f"\nГород: {advert.city_name}" if advert.city_name else ""
            fund_text = f"\nФонд: {advert.fund_name}" if advert.fund_name else ""
        
            text = f"**{advert.title or 'Объявление'}{urgency_text}**\n{advert.description}\n\n{progress_text}{location_text}{fund_text}\n\nВведите сумму пожертвования (например: 500):"
            body = NewMessageBody(text=text, format="markdown")
            await self.client.send_message(chat_id, body)
            return
        
        if state == UserState.DONATION_ENTERING_AMOUNT and text_input:
            print(f"DEBUG donations: Processing amount = '{text_input}' for {user_id}")
            try:
                amount = float(text_input.strip())
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной.")
            except ValueError as e:
                body = NewMessageBody(text=f"Неверная сумма: {e}. Введите число (например: 500):")
                await self.client.send_message(chat_id, body)
                return
            
            advert_id = data.get("selected_advert_id")
            all_adverts = data.get("adverts", [])
            advert = next((a for a in all_adverts if str(a.id) == advert_id), None)
            if not advert:
                await self.client.send_message(chat_id, NewMessageBody(text="Объявление не найдено."))
                await fsm.clear_state(user_id)
                return
            
            link = await client.generate_donation_link(advert)
            #await self.repo.save_donation(user_id, amount, advert.title or "Объявление", link) # уберем сохранение доната
            progress_text = f"\nТекущий прогресс: {advert.money_collected:,} ₽ ({advert.percent}%)" if advert.money_collected and advert.percent else ""
            text = f"**Пожертвование в '{advert.title or 'Объявление'}':**\nСумма: {amount} ₽{progress_text}\n\n[Перейти к донату]({link})"
            buttons = [
                [Button(type="link", text="Открыть ссылку", url=link)],
                [Button(type="callback", text="Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text=text, format="markdown")
            await self.client.send_message(chat_id, body, buttons)
            await fsm.clear_state(user_id)
            return

        # Fallback
        print(f"DEBUG donations: Fallback triggered for payload={payload}, state={state}")
        await fsm.clear_state(user_id)
        body = NewMessageBody(text="Донат отменён. Начните заново.")
        buttons = [[Button(type="callback", text="Донат", payload="donate")]]
        await self.client.send_message(chat_id, body, buttons)
