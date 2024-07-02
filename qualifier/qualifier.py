from enum import auto, StrEnum

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    ...


# Implement the class below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        ...

    def __str__(self) -> str:
        ...


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    ...


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return cls.quotes

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in cls.quotes:
            raise DuplicateError
        cls.quotes.append(quote)
