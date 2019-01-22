import asyncio
import logging
import traceback

from libs import eve_pi_libs

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <eve_pi.py>: Monitor and track EVE PI.")

ledger_manager = eve_pi_libs.LedgerManager()

help_str = """
** EVE PI Bot **
```
!epi help - this message
```
"""

filling_ledger = False


@asyncio.coroutine
async def action(**kwargs):
    global filling_ledger
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    try:
        if filling_ledger:
            await message.channel.send("`Parsing PI inventory...`")
            ledger_manager.reset_stock(message.content)
            filling_ledger = False
            await message.channel.send("`Completed parsing PI inventory!`")


        split_content = message.content.split()

        if split_content[0] == '!epi':

            if len(split_content) == 2:
                if split_content[1] == 'help':
                    await message.channel.send(help_str)
                if split_content[1] == 'ledger':
                    filling_ledger = True
                    await message.channel.send("`Copy/paste your PI inventory from your ships hold...`")


    except:
        print(traceback.format_exc())
