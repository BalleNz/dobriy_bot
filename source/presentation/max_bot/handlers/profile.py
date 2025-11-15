from source.presentation.max_bot.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max_bot.states.fsm import UserState, fsm

from datetime import datetime
from typing import Dict

from source.infrastructure.dishka import make_dishka_container
from source.application.profile.get_by_id import GetUserProfileById
from source.application.profile.merge import MergeUserProfile
from source.application.profile.create_or_update import CreateOrUpdateProfile
from source.application.user.create_or_update import CreateOrUpdateUser


#from source.application.user
from source.core.schemas.profile import ProfileSchema
from source.core.schemas.user import UserSchema




class ProfileHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        _, payload, _ = self._parse_update(update)
        return (
            payload == "profile" or
            payload == "edit_profile" or
            state in [UserState.EDITING_BIRTH_DATE, UserState.EDITING_INTERESTS]
        )

    async def handle(self, update: Dict, user_id: int, chat_id: int):
        dishka_container = make_dishka_container()
        create_or_update = await dishka_container.get(CreateOrUpdateProfile)
        get_user = await dishka_container.get(CreateOrUpdateUser)

        state = await fsm.get_state(user_id)
        _, payload, text_input = self._parse_update(update)

        if payload == "profile":
            profile: ProfileSchema = await create_or_update(user_id)
            user: UserSchema = await get_user(user_id)
            
            name = f"{user.first_name} {user.last_name or ''}".strip()
            name = "Маркарян"
            birth_text = profile.birthday or "Не указана"
            interests_text = profile.interests or "Не указаны"
            text = f"👤 **Профиль**\n\nИмя: {name}\nДата рождения: {birth_text}\nИнтересы: {interests_text}"
            buttons = [
                [Button(type="callback", text="Изменить профиль", payload="edit_profile")],
                [Button(type="callback", text="🔙 Главное меню", payload="main_menu")]
            ]
            body = NewMessageBody(text=text, format="markdown")
            await self.client.send_message(chat_id, body, buttons)
            return

        if payload == "edit_profile":
            await fsm.set_state(user_id, UserState.EDITING_BIRTH_DATE)
            body = NewMessageBody(text="Введите дату рождения в формате ДД.ММ.ГГГГ (например, 15.11.2000):")
            await self.client.send_message(chat_id, body)
            return

        if state == UserState.EDITING_BIRTH_DATE and text_input:
            try:
                dt = datetime.strptime(text_input.strip(), '%d.%m.%Y')
                birth_date = dt.strftime('%d.%m.%Y')
                await create_or_update(ProfileSchema(
                    user_id=user_id,
                    birthday=birth_date
                ))
                await fsm.set_state(user_id, UserState.EDITING_INTERESTS)
                body = NewMessageBody(text="Дата рождения обновлена! Теперь введите ваши интересы (через запятую, например: животные, дети, экология):")
                await self.client.send_message(chat_id, body)
            except ValueError:
                body = NewMessageBody(text="Неверный формат даты. Введите в формате ДД.ММ.ГГГГ:")
                await self.client.send_message(chat_id, body)
            return

        if state == UserState.EDITING_INTERESTS and text_input:
            interests = text_input.strip()
            await create_or_update(ProfileSchema(
                                            user_id=user_id,
                                                 interests=interests)
                                                 )
            await fsm.clear_state(user_id)
            body = NewMessageBody(text="Интересы обновлены! Ваш профиль обновлен.")
            buttons = [[Button(type="callback", text="👤 Профиль", payload="profile")]]
            await self.client.send_message(chat_id, body, buttons)
            return

        body = NewMessageBody(text="Не понял. Вернитесь в профиль.")
        buttons = [[Button(type="callback", text="👤 Профиль", payload="profile")]]
        await self.client.send_message(chat_id, body, buttons)
