from discord.ext import tasks

from libs.task_router import TaskRouter


@TaskRouter("examples")
@tasks.loop(seconds=5)
async def example_periodic_task() -> None:
    """Example task that runs every 5 seconds."""
    print("Example periodic task is running!")


@TaskRouter("examples")
@tasks.loop(seconds=10)
async def example_hourly_task() -> None:
    """Example task that runs every 10 seconds."""
    print("Example hourly task is running!")

