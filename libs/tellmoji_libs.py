import random
from collections import deque
from inspect import cleandoc


class TellmojiMatch:
    emoji_dict = {
        "sword": "⚔",
        "shield": "🛡",
        "crown": "👑",
        "flag": "🚩",
        "knight": "🐴",
        "hammer": "🔨",
        "scales": "⚖"
    }

    def __init__(self, member_list):
        self.players = member_list
        self.p1_score = 0
        self.p2_score = 0
        self.pool = deque(['sword', 'shield', 'crown', 'flag', 'knight', 'hammer', 'scales'])
        self.line = deque([])
        self.flipped = {
            'sword': False,
            'shield': False,
            'crown': False,
            'flag': False,
            'knight': False,
            'hammer': False,
            'scales': False
        }
        self.game_state = 'READY'

    def gameboard_message(self):
        """
        Translates the game board into a sendable Discord message
        """
        # generate the line portion of the message
        pool_str = ' '.join([self.emoji_dict[icon] for icon in self.pool])
        line_str = ' '.join([self.emoji_dict[icon] if not self.flipped[icon] else '❓' for icon in self.line])
        line_msg = f"""```
        {self.players[0].name}: {self.p1_score}
        ```
        **Line**: {line_str}
        ```
        {self.players[1].name}: {self.p2_score}
        ```
        **Pool:** {pool_str}
        """

        return cleandoc(line_msg)

    def add_to_line(self, target_emoji, direction):
        valid_directions = ['l', 'r']

        if target_emoji in self.pool and direction in valid_directions:
            self.pool.remove(target_emoji)

            if direction == 'l':
                self.line.appendleft(target_emoji)
                return True
            elif direction == 'r':
                self.line.append(target_emoji)
                return True
        else:
            return False

    def boast(self, index, guess):
        return self.line[index] == guess

    def hide(self, target_emoji):
        if not self.flipped[target_emoji] and target_emoji in self.line:
            self.flipped[target_emoji] = True
            return True
        else:
            return False

    def peek(self, target):
        is_hidden = [self.flipped[token] for token in self.line]
        if len(self.line) >= target:
            if is_hidden[target]:
                return self.line[target]

    def switch(self, target_1, target_2):
        if len(self.line) >= 2:
            temp = self.line[target_1]
            self.line[target_1] = self.line[target_2]
            self.line[target_2] = temp


def test_tellmoji():
    class Player:
        def __init__(self, name):
            self.name = name

    # Create the Match
    p1 = Player("Player1")
    p2 = Player("Player2")
    tm = TellmojiMatch([p1, p2])

    # Make some moves
    tm.add_to_line('knight', 'l')
    tm.add_to_line('crown', 'l')
    tm.add_to_line('hammer', 'r')
    tm.hide('hammer')
    print(tm.gameboard_message())
    print(tm.peek(2))
    print('\n\n')
    tm.switch(0, 1)
    print(tm.gameboard_message())
    print(tm.boast(0, 'crown'))
    print(tm.boast(2, 'hammer'))
