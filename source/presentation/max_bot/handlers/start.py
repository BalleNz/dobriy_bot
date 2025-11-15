from source.presentation.max_bot.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max_bot.states.fsm import UserState, fsm
from source.presentation.max_bot.keyboards.keyboards import MAIN_MENU_BUTTONS
from source.application.user.create_or_update import CreateOrUpdateUser
from source.infrastructure.dishka import make_dishka_container
from source.core.schemas.user import UserSchema


from typing import Dict

class StartHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        update_type, _, text = self._parse_update(update=update)
        return update_type == "bot_started" or text == "/start" 

    async def handle(self, update: Dict, user_id: int, chat_id: int):  
        print(f"StartHandler: Handling for user_id={user_id}, chat_id={chat_id}")
        dishka_container = make_dishka_container()
        async with dishka_container() as req_container:
            get_user = await req_container.get(CreateOrUpdateUser)  # Теперь factory на REQUEST доступен
            
            update_type, _, _ = self._parse_update(update)
            
            if update_type == "bot_started":
                user_data = update["user"]
            else:
                user_data = update["message"]["sender"]
            
            user_schema = UserSchema(
                max_id=str(user_id),
                username=user_data.get("name"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name")
            )
            
            updated_user = await get_user(user_schema)  # Вызов внутри scope
        
        # ← Scope exited: REQUEST-deps (UoW, repo) автоматически финализируются (закрыты)
        
        body = NewMessageBody(text="**Я — Добрый помощник!**\n\nЯ помогу вам с благотворительностью.", format="markdown")
        await self.client.send_message(chat_id, body, MAIN_MENU_BUTTONS)
        await fsm.set_state(user_id, UserState.IDLE)