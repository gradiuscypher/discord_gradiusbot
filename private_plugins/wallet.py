from libs.wallet import Wallet
import asyncio


print("[Private Plugin] <wallet.py>: The GradiusCoin wallet.")

help_message = """
__**!wallet help** (PM Only)__

Your GradiusCoin wallet. Collect GradiusCoin, spend GradiusCoin, give GradiusCoin.

Examples:
!wallet

Show your wallet balance.


"""

wallet = Wallet()


@asyncio.coroutine
def action(message, client, config):
    sender = message.author.id
    content = message.content
    split_content = content.split()

    if split_content[0] == "!wallet":

        if len(split_content) == 1:
            balance = wallet.get_balance(sender)
            yield from client.send_message(message.channel, "Your balance: {} GradiusCoins".format(balance))
