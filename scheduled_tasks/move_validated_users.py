import asyncio

print("[Scheduled Task] <move_validated_users.py>: Moves validated users from 'not_validated' to 'member'.")


@asyncio.coroutine
def action(client, config):
    while True:
        # Check for users in the not_validated role
        # Check to see if their discord name exists in the gdusers database and is validated to a summoner name
        # If validated, remove the not_validated role and move to member role
        yield from asyncio.sleep(30)
