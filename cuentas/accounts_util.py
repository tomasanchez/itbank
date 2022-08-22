import random

from django.contrib.staticfiles.storage import StaticFilesStorage


def generate_alias() -> str:
    """
        Create a random alias for a new account.
    """
    s = StaticFilesStorage()
    words = s.open('homebanking/data/words.txt', 'rb+').read().splitlines()
    return f"{random.choice(words).decode('utf-8')}" \
           f".{random.choice(words).decode('utf-8')}" \
           f".{random.choice(words).decode('utf-8')}"
