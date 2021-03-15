# TODO: need a scheduled task to periodically pull from the Thera site and determine if an alert needs to be sent
# TODO: add a filter to alert when there's a WH X number of jumps away from a system
# TODO: finish commands

import logging
import requests
from libs.eve import solarsystem


logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <thera.py> Alerts a user of an open Thera WH in the spaces they configure")

alerts = solarsystem.WhAlert()


"""
expected workflow:
- user sets up an alert
  - start can be a specific system, HS, LS, WH, or * for a wildcard
  - end can be a specific system, HS, LS, WH, or a * for wild card
"""

help_message = """```\n**WH Alert System Help**\n
Allows the user to track the appearance of WHs that connect to and from Thera space. Powered by `eve-scout.com`. Updates every 15 minutes.

<START_SYSTEM_NAME> can be one of four values: The system name, HS (for all high sec WHs), LS (for all low sec WHs), or * (for all WHs)
<END_SYSTEM_NAME> can be one of four values: The system name, HS (for all high sec WHs), LS (for all low sec WHs), or * (for all WHs)

!wh help - this message
!wh list - list all active alerts
!wh add <START_SYSTEM_NAME> <END_SYSTEM_NAME> - add an alert
!wh remove <ALERT_ID> - remove an active alert by ALERT_ID

For example, to add a new WH alert for all high sec exits when there is a connection to O3Z5-G:
!wh add O3Z5-G HS

For example, to remove your 3rd alert:
!wh remove 3
```
"""

async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = [s.lower() for s in message.content.split()]


    try:
        if len(split_message) > 1:
            if split_message[0] == '!wh':
                if split_message[1] == 'add':
                    try:
                        result = alerts.add_alert()
                    except:
                        pass
                if split_message[1] == 'remove':
                    try:
                        result = alerts.remove_alert()
                    except:
                        pass

                if split_message[1] == 'list':
                    try:
                        pass
                    except:
                        pass

                if split_message[1] == 'help':
                    try:
                        pass
                    except:
                        pass

    except:
        pass