from discord import Message

from libs.router import MessageRouter, MessageType


@MessageRouter("examples", MessageType.message)
async def message_testtest(message: Message):
    print(f"message_test: {message.content}")
    await message.channel.send(f"I'm here! - {message.content}")


@MessageRouter("examples", MessageType.message)
async def another(message: Message):
    print(f"another: {message.content}")


@MessageRouter("examples", MessageType.dm)
async def dm_test_one(message: Message):
    print(f"dm_test_one: {message.content}")


@MessageRouter("examples", MessageType.dm)
async def dm_test_two(message: Message):
    print(f"dm_test_two: {message.content}")
