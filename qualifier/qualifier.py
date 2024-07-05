import re
from enum import auto, StrEnum
import logging
import warnings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


# print(VariantMode['NORMAL'])


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode
        self.processed = False

    def __str__(self) -> str:
        return self._create_variant()

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        if not self.processed:
            self.quote = getattr(self, self.mode)()
            self.processed = True
        return self.quote

    def normal(self) -> str:
        return self.quote

    def uwu(self) -> str:
        """
        uwu-ify the quote and return the result
        """

        # L/l -→ W/w and R/r → W/w
        quote = self.quote.translate(
            str.maketrans({
                'l': 'w',
                'r': 'w',
                'L': 'W',
                'R': 'W',
            })
        )

        quote_with_stutter_list = []
        for word in quote.split(" "):
            if word.lower().startswith("u"):
                quote_with_stutter_list.append(f"{word[0]}-{word}")
            else:
                quote_with_stutter_list.append(word)
        quote = " ".join(quote_with_stutter_list)

        if len(quote) > MAX_QUOTE_LENGTH:
            warnings.warn("Quote too long, only partially transformed")

        if self.quote == quote:
            raise ValueError("Quote was not modified")

        self.quote = quote
        return self.quote



    def piglatin(self) -> str:
        return self.quote


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

    # space at the end is important,
    # as we need to check for the word 'quote' at the start of the command
    ROOT_COMMAND = 'quote '
    if command[:len(ROOT_COMMAND)] != ROOT_COMMAND:
        raise ValueError('Invalid command')

    command = command[len(ROOT_COMMAND):].strip()

    COMMAND_REGEX = r'([A-Za-z]*)\s*(?:["“](.*)["”])?'
    result = re.findall(COMMAND_REGEX, command)
    logger.debug(result)
    sub_command, quote = re.match(COMMAND_REGEX, command).groups()
    if not sub_command:
        sub_command = ''
    if not quote:
        quote = ''

    sub_command_length = len(sub_command)
    quote_length = len(quote)

    if sub_command_length == 0:
        sub_command = 'normal'

    if sub_command == 'list':
        print("- " + "\n- ".join(Database.get_quotes()))
        return

    if quote_length == 0:
        raise ValueError('Quote is missing')

    if quote_length > MAX_QUOTE_LENGTH:
        raise ValueError('Quote is too long')

    if sub_command not in VariantMode:
        raise ValueError('Invalid command')

    try:
        Database.add_quote(
            Quote(
                quote, VariantMode[sub_command.upper()]
            )
        )
    except DuplicateError:
        print("Quote has already been added previously")


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
