""" Unit testing for the Omega-Robot """

import json
import unittest
import re
from emoji import UNICODE_EMOJI


def test_emoji(string):
    """ Test string against Discord emojis RegEx and Unicode emojis list """
    emoji_in_msg = bool(re.search(r"<a?:.+?:\d+>|<:.+?:\d+>|:[a-z_]+:", string))
    for i in list(string):
        emoji_in_msg += i in UNICODE_EMOJI["en"]

    return bool(emoji_in_msg)


class RegexTest(unittest.TestCase):
    """ Test RegEx patterns against common cases """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("config.json", encoding="utf-8") as file:
            config = json.load(file)

        self.regex_patterns = {chan_id: re.compile(pattern)
                               for chan_id, pattern in config["REGEX_CHANNELS"].items()}

    def test_rage_banned(self):
        """ Test banned strings against Rage channel RegEx """
        banned = ["AbcDefG", "hello world", "дгват", "ça va ?"]

        for i in banned:
            self.assertFalse(
                self.regex_patterns["718924415361876075"].fullmatch(i))

    def test_rage_allowed(self):
        """ Test allowed strings against Rage channel RegEx """
        allowed = ["EA SPORTS", "https://archlinux.org",
                   "🏳️‍⚧️", "PIEW !", "РПИЗЄФ"]

        for i in allowed:
            self.assertTrue(
                self.regex_patterns["718924415361876075"].fullmatch(i))

    def test_pleaseimlost_banned(self):
        """ Test banned strings against PleaseImLost channel RegEx """
        banned = ["AbcDefG", "hello world", "дгват", "ça va ?", "🏳️‍⚧️"]

        for i in banned:
            self.assertFalse(
                self.regex_patterns["720374386955255818"].fullmatch(i))

    def test_pleaseimlost_allowed(self):
        """ Test allowed strings against PleaseImLost channel RegEx """
        allowed = [
            "https://cdn.discordapp.com/attachments/720374386955255818/865578710107291678/IMG_20210716_150030.jpg",
            "https://archlinux.org",
            "https://cdn.discordapp.com/attachments/720374386955255818/865344852849590282/video0-32-1.mp4",
            "https://twitter.com/Cosmicabuse/status/1415013563559723013?s=19",
            "https://youtu.be/atq_7zDnQ1A"
        ]

        for i in allowed:
            self.assertTrue(
                self.regex_patterns["720374386955255818"].fullmatch(i))

    def test_confession_refused(self):
        """ Test refused strings against Confession channel RegEx """
        allowed = ["Heyy :ok_hand:", "Ow 😩😩", "🏳️‍⚧️",
                   "👉📸👈", "Hahaha <:troll:685948400591437858>"]

        for i in allowed:
            self.assertTrue(
                test_emoji(i))

    def test_confession_allowed(self):
        """ Test allowed strings against Confession channel RegEx """
        allowed = ["It's in the game", "I luv https://archlinux.org",
                   "Wow wow, my life is incredible", "U Just Lost The Game", "Права Транс"]

        for i in allowed:
            self.assertFalse(
                test_emoji(i))


if __name__ == '__main__':
    unittest.main()
