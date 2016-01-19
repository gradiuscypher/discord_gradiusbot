# TODO: Finish implementation
# TODO: Add validation table to keep track of when someone validates a song, to encourage voting

import sqlite3


class AmplitudeLib:

    def __init__(self):
        print("Loaded AmplitudeLib")
        self.connection = sqlite3.connect('amplitude.db')
        self.connection.row_factory = sqlite3.Row

    def build_db(self):
        song_list = [
            "Perfect Brain",
            "Wetware",
            "Dreamer",
            "Recession",
            "Break For Me",
            "Decode Me",
            "I.C.U.",
            "Human Love",
            "Astrosight",
            "Magpie",
            "Supraspatial",
            "Digital Paralysis",
            "Energize",
            "Dalatecht",
            "Wayfarer",
            "All The Time",
            "Assault on Psychofortress",
            "Concept",
            "Crazy Ride",
            "Crypteque (1-2)",
            "Crystal",
            "Do Not Retreat",
            "Entomophobia",
            "Force Quit",
            "Impossible",
            "Lights",
            "Muze (Amplitude Remix)",
            "Phantoms",
            "Red Giant",
            "Synthesized (Inside Your Mind Remix)",
            "Unfinished Business"
        ]
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE scores(id INTEGER, song text, user text, score INTEGER, link text, validations INTEGER)")
        self.connection.commit()

        cursor = self.connection.cursor()
        song_id = 0

        for song in song_list:
            cursor.execute("insert into scores values(?, ?, 'None', 0, 'None', 0)", (song_id, song,))
            song_id += 1

        self.connection.commit()

    def get_score_list(self):
        score_dict = {}
        cursor = self.connection.cursor()
        query = cursor.execute("select * from scores")
        scores = query.fetchall()

        for score in scores:
            score_dict[score['id']] = {"song": score['song'], "user": score['user'], "score": score['score'],
                                       "link": score['link'], "validations": score['validations']}

        return score_dict

    def validate_score(self, song_id):
        # Allow the user to vote to validate the song.
        print("Validated")

    def report_score(self, song_id):
        # Allow the user to report a false score.
        print("Reported")

    def update_score(self, song_id, score, user, link):
        # Allow the user to report a new high score
        print("Updated")
