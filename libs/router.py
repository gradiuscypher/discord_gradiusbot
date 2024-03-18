from enum import Enum
from typing import Callable

from discord import Message


class MessageType(Enum):
    dm = 0
    message = 1


class MessageRouter:
    _func_map: dict[MessageType, list[tuple[str, Callable]]] = {}

    def __init__(self, module_group: str, message_type: MessageType):
        self.message_type = message_type
        self.module_group = module_group

    def __call__(self, f: Callable):
        if self.message_type in self._func_map:
            self._func_map[self.message_type].append((self.module_group, f))
        else:
            self._func_map[self.message_type] = [(self.module_group, f)]

        return f

    @classmethod
    async def route(
        cls, enabled_modules: list[str], message_type: MessageType, message: Message
    ):
        functions = cls._func_map.get(message_type)

        if functions:
            for f_tuple in functions:
                if f_tuple[0] in enabled_modules:
                    await f_tuple[1](message)
