from enum import Enum
from typing import Callable

from discord import Message


class MessageType(Enum):
    dm = 0
    message = 1


class MessageRouter:
    _func_map: dict[MessageType, list[Callable]] = {}

    def __init__(self, tag: MessageType):
        self.tag = tag

    def __call__(self, f: Callable):
        if self.tag in self._func_map:
            self._func_map[self.tag].append(f)
        else:
            self._func_map[self.tag] = [f]

        return f

    @classmethod
    async def route(cls, tag: MessageType, message: Message):
        functions = cls._func_map.get(tag)

        if functions:
            for f in functions:
                await f(message)
