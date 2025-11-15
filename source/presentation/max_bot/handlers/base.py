from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional

from source.infrastructure.database.repo.user_repo import UserRepository
from source.infrastructure.max.api_client import MaxBotClient
from source.presentation.max_bot.states.fsm import UserState


class BaseHandler(ABC):
    def __init__(self, client: MaxBotClient):
        self.client = client

    @abstractmethod
    async def handle(self, update: Dict, user_id: int, chat_id: int):
        pass

    @abstractmethod
    def can_handle(self, update: Dict, state: UserState) -> bool:
        pass

    @staticmethod
    def _parse_update(update: Dict) -> Tuple[str, Optional[str], Optional[str]]:
        update_type = update.get("update_type", "")
        payload = None
        text = None

        if update_type == "message_callback":
            payload = update.get("callback", {}).get("payload")
        elif update_type == "message_created":
            text = update.get("message", {}).get("body", {}).get("text")

        return update_type, payload, text
