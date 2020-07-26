async def example_action_1(**kwargs):
    message = kwargs['message']

    print("EXAMPLE ACTION 1")
    await message.channel.send("THIS IS AN EXAMPLE ACTION1")
