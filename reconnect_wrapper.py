#! venv3/bin/python

import gradiusbot
import sys
import traceback
import time


if __name__ == "__main__":
    reconnect = 2
    tried = 0
    while tried <= reconnect:

        try:
            gradiusbot.main_task(sys.argv[1])

        except:
            print(traceback.print_exc())
            time.sleep(2)
            tried += 1
