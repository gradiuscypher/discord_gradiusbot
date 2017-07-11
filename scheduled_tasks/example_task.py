import asyncio

print("[Scheduled Task] <example_task.py>: This is a scheduled background task.")


@asyncio.coroutine
def action(client, config):
    while True:
        print("This is an example of a scheduled task being executed.")
        yield from asyncio.sleep(5)
