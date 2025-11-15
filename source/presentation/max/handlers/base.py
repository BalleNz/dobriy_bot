from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from source.presentation.max.states.fsm import UserState
from source.infrastructure.max.api_client import NewMessageBody, MaxBotClient

class BaseHandler(ABC):
    def __init__(self, client: MaxBotClient, repo: int):
        self.client = client
        self.repo = repo

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