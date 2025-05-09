import os
import random

from discord import Message
from dotenv import load_dotenv

from libs.router import MessageRouter, MessageType

load_dotenv()  # load all the variables from the env file
someone_id = os.getenv("SOMEONE_ID", None)


@MessageRouter("memes", MessageType.message)
async def lol(message: Message):
    if (
        message.content in ["lol", "lol.", "lmao", "lmao."]
        and random.randint(0, 100) >= 99
    ):
        await message.channel.send("lol")


@MessageRouter("memes", MessageType.message)
async def someone(message: Message):
    if "someone" in message.content and random.randint(0, 1000) >= 999 and someone_id:
        await message.reply(f"<@{someone_id}> is this true?")
