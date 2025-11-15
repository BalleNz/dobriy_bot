from source.infrastructure.max.api_client import MaxBotClient, NewMessageBody
from source.presentation.max.handlers import *
#from source import Notifier
from source.presentation.max.states.fsm import fsm
from source.presentation.max.keyboards.keyboards import MAIN_MENU_BUTTONS
from source.infrastructure.dishka.__init_ import make_dishka_container

import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HANDLERS = [StartHandler, ProblemsHandler, ResultsHandler, HelpChoiceHandler, FundChoiceHandler, NotificationsHandler, ProfileHandler, PrivacyHandler, SupportHandler, DonationsHandler]


async def main():
    dishka_container = make_dishka_container()
    maxbot = await dishka_container.get(MaxBotClient)

    async with maxbot as client:
        repo = 1
        #notifier = Notifier(client, repo)
        #notifier.start()

        marker = None
        while True:
            try:
                updates = await client.get_updates(marker)
                if "updates" in updates:
                    for update in updates["updates"]:
                        marker = update.get("marker")
                        
                        # Извлечение user_id/chat_id (human sender)
                        update_type = update.get("update_type")
                        if update_type == "bot_started":
                            user_id = update["user"]["user_id"]
                            chat_id = update["chat_id"]
                        elif update_type == "message_created":
                            message = update.get("message", {})
                            user_id = message.get("sender", {}).get("user_id")
                            chat_id = message.get("recipient", {}).get("chat_id")
                        elif update_type == "message_callback":
                            callback = update.get("callback", {})
                            user_id = callback.get("user", {}).get("user_id")  # Human who clicked
                            message = update.get("message", {})
                            chat_id = message.get("recipient", {}).get("chat_id")
                        else:
                            user_id = update.get("user", {}).get("user_id", 0)
                            chat_id = update.get("chat_id", 0)
                        
                        logger.debug(f"Update: type={update_type}, user_id={user_id}, chat_id={chat_id}")

                        state = await fsm.get_state(user_id)

                        handled = False
                        for handler_class in HANDLERS:
                            handler = handler_class(client, repo)
                            if handler.can_handle(update, state):
                                logger.info(f"Handling in {handler_class.__name__} for user_id={user_id}")
                                await handler.handle(update, user_id, chat_id)
                                handled = True
                                break

                        # Fallback для /start
                        if not handled:
                            update_type, _, text = BaseHandler._parse_update(update)
                            if text == "/start":
                                logger.info("Fallback: /start for user_id={user_id}")
                                await StartHandler(client, repo).handle(update, user_id, chat_id)
                                handled = True

                        if not handled and update.get("callback", {}).get("payload") == "main_menu":
                            logger.info("Fallback: main_menu for user_id={user_id}")
                            body = NewMessageBody(text="Главное меню")
                            await client.send_message(chat_id, body, MAIN_MENU_BUTTONS)

                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Loop error: {e}", exc_info=True)  # Полный traceback
                await asyncio.sleep(5)  # Retry delay

if __name__ == "__main__":
    asyncio.run(main())