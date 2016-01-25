#! venv3/bin/python

import subprocess
import sys
import time


if __name__ == "__main__":
    config_file = sys.argv[1]
    try_reconnect = True

    while try_reconnect:
        still_running = True

        print("Connecting the bot...")
        process = subprocess.Popen(['venv3/bin/python', 'gradiusbot.py', config_file], stdout=subprocess.PIPE)
        process.communicate()

        print("We're done being a bot.")
        time.sleep(10)
