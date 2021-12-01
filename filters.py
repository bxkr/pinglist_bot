import re

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message, Chat, CallbackQuery


class ChatType(BaseFilter):
    chat_type: str

    async def __call__(self, message: Message, event_chat: Chat) -> bool:
        if event_chat:
            if self.chat_type == 'group':
                return event_chat.type == self.chat_type or event_chat.type == 'supergroup'
            else:
                return event_chat.type == self.chat_type
        else:
            return False


class RegExp(BaseFilter):
    re: str

    async def __call__(self, callback: CallbackQuery) -> bool:
        return bool(re.match(self.re, callback.data))
