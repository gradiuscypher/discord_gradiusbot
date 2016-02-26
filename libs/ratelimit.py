import time


class RateLimit:

    def __init__(self):
        self.command_timers = {}

    def add_command_ratelimit(self, command, limit):
        self.command_timers[command] = (time.time(), limit)

    def can_use_command(self, command):
        current_time = time.time()
        command_timer = self.command_timers[command]

        if current_time - command_timer[0] > command_timer[1]:
            self.command_timers[command] = (time.time(), command_timer[1])
            return True
        else:
            return False
