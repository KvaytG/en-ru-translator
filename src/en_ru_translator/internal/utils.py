import re

_ENGLISH_LETTERS = re.compile(r"[a-zA-Z]")


def has_english_letters(text: str):
    """ INTERNAL FUNCTION! """
    return bool(_ENGLISH_LETTERS.search(text))
