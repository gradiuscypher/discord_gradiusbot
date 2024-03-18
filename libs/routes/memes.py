import random

from discord import Message

from libs.router import MessageRouter, MessageType


@MessageRouter("memes", MessageType.message)
async def lol(message: Message):
    if (
        message.content in ["lol", "lol.", "lmao", "lmao."]
        and random.randint(0, 100) >= 95
    ):
        await message.channel.send("lol")
