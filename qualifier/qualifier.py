from enum import auto, StrEnum
import warnings

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
            # Perform the L/l→W/w and R/r→W/w conversions first
            transformed = (
                self.quote.replace("l", "w")
                .replace("r", "w")
                .replace("L", "W")
                .replace("R", "W")
            )

            # If the transformed quote too long, issue a warning; return it
            if len(transformed) > MAX_QUOTE_LENGTH:
                warnings.warn("Quote too long, only partially transformed", Warning)
                return transformed[:MAX_QUOTE_LENGTH]

            # Perform the U/u "stutter" transformation only if the length allows
            words = transformed.split()
            stuttered_words = []
            for i, word in enumerate(words):
                if word.lower().startswith("u"):
                    stuttered_word = f"{word[0]}-{word}"
                    potential_length = len(
                        " ".join(stuttered_words + [stuttered_word] + words[i + 1 :])
                    )
                    if potential_length <= MAX_QUOTE_LENGTH:
                        stuttered_words.append(stuttered_word)
                    else:
                        stuttered_words.append(word)
                        warnings.warn(
                            "Quote too long, only partially transformed", Warning
                        )
                        break
                else:
                    stuttered_words.append(word)

            transformed = " ".join(stuttered_words)

            if transformed == self.quote:
                raise ValueError("Quote was not modified")

            return transformed

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

            transformed = " ".join(piglatin_words).capitalize()

            if len(transformed) > MAX_QUOTE_LENGTH:
                raise ValueError("Quote was not modified")

            return transformed

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

    command_parts = command.split(maxsplit=1)
    if len(command_parts) < 1:
        raise ValueError("Invalid command")

    action = command_parts[0]

    if action != "quote":
        raise ValueError("Invalid command")

    quote_text = command_parts[1] if len(command_parts) > 1 else ""
    quote_parts = quote_text.split(maxsplit=1)

    mode = VariantMode.NORMAL
    if len(quote_parts) > 1 and quote_parts[0] in ["uwu", "piglatin"]:
        mode_str, quote_text = quote_parts
        if mode_str == "uwu":
            mode = VariantMode.UWU
        elif mode_str == "piglatin":
            mode = VariantMode.PIGLATIN

    elif len(quote_parts) == 1 and quote_parts[0] in ["list"]:
        quotes = Database.get_quotes()
        for quote in quotes:
            print(f"- {quote}")
    # Removing the wrapping quotes
    if (quote_text.startswith('"') and quote_text.endswith('"')) or (
        quote_text.startswith("“") and quote_text.endswith("”")
    ):
        quote_text = quote_text[1:-1]

    if len(quote_text) > MAX_QUOTE_LENGTH:
        raise ValueError("Quote is too long")

    quote = Quote(quote_text, mode)
    transformed_quote = str(quote)

    if action in ["quote"] and mode != VariantMode.NORMAL:
        if transformed_quote == quote_text:
            raise ValueError("Quote was not modified")
        if len(transformed_quote) > MAX_QUOTE_LENGTH:
            warnings.warn("Quote too long, only partially transformed", Warning)
            transformed_quote = transformed_quote[:MAX_QUOTE_LENGTH]

    try:
        Database.add_quote(quote)
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
