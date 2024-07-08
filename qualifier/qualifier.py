from enum import auto, StrEnum

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode

    def __str__(self) -> str:
        return self._create_variant()

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """

        if self.mode == VariantMode.UWU:
            uwu_translation = (
                self.quote.replace("l", "w")
                .replace("r", "w")
                .replace("L", "W")
                .replace("R", "W")
            )
            return uwu_translation
        elif self.mode == VariantMode.PIGLATIN:
            vowels = "AEIOUaeiou"
            words = self.quote.split()
            piglatin_words = []

            for word in words:
                if word[0] in vowels:
                    piglatin_word = word + "way"
                else:
                    for i, letter in enumerate(word):
                        if letter in vowels:
                            piglatin_word = word[i:] + word[:i] + "ay"
                            break
                    else:
                        piglatin_word = word + "ay"  # For words without vowels
                piglatin_words.append(piglatin_word)

            return " ".join(piglatin_words)
        else:
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
    command_items = command.split(maxsplit=2)

    if len(command_items) < 2:
        print("Invalid command")
        return

    # Break up commmand in to 2 parts: action (i.e quote) and text (i.e "My quote")
    action = command_items[1]
    quote_text = command_items[2] if len(command_items) > 2 else ""

    if action == "list":
        # Retrieve quotes via 'Database' fetch
        quotes = Database.get_quotes()

        for i, quote in enumerate(quotes):
            print(f"{id}=> {quote}")


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
