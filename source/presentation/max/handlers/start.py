from source.presentation.max.handlers import BaseHandler
from source.infrastructure.max.api_client import Button, NewMessageBody
from source.presentation.max.states.fsm import UserState, fsm
from source.presentation.max.keyboards.keyboards import MAIN_MENU_BUTTONS

from typing import Dict

class StartHandler(BaseHandler):
    def can_handle(self, update: Dict, state: UserState) -> bool:
        update_type, _, text = self._parse_update(update=update)
        return update_type == "bot_started" or text == "/start" 

    async def handle(self, update: Dict, user_id: int, chat_id: int):  
        print(f"StartHandler: Handling for user_id={user_id}, chat_id={chat_id}")
        
        update_type, _, _ = self._parse_update(update)
        
        if update_type == "bot_started":
            user_data = update["user"]
        else:
            user_data = update["message"]["sender"]
        
       # user = await self.repo.get_or_create_user(
       #     user_id, user_data["first_name"], user_data.get("last_name"), user_data.get("username")
        #)
        
        body = NewMessageBody(text="**Я — Добрый помощник!**\n\nЯ помогу вам с благотворительностью.")
        await self.client.send_message(chat_id, body, MAIN_MENU_BUTTONS)  # ← chat_id
        await fsm.set_state(user_id, UserState.IDLE)