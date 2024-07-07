from enum import auto, StrEnum
import re
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
        return self.quote

        

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        if self.mode == VariantMode.NORMAL:
            return self.quote
        elif self.mode == VariantMode.PIGLATIN:
            words = []
            vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

            for word in self.quote.split(" "):
                upperCase = word[0].isupper()

                if word[0] in vowels:
                    word = word + "way"
                else:
                    cluster = ""
                    index = 0
                    for letter in word:
                        if letter in vowels:
                            break
                        cluster += letter
                        index += 1
                    word = word[index:] + cluster.lower() + "ay"

                if upperCase:
                    word = word[0].upper() + word[1:] 
                words.append(word)

            piglatin_quote = " ".join(words)

            if len(piglatin_quote) > MAX_QUOTE_LENGTH:
                raise ValueError("Quote was not modified")

            return piglatin_quote
                
        elif self.mode == VariantMode.UWU:
            uwu_quote = ""

            if re.search('[lLrRuU]', self.quote):

                for char in self.quote:
                    if char in ['l', 'r']:
                        char = 'w'
                    elif char in ['L', 'R']:
                        char = 'W'
                    uwu_quote += char

                temp_quote = ""
                words = []
                for word in uwu_quote.split(" "):
                    if word.startswith("u"):
                        word = "u-" + word
                    elif word.startswith("U"):
                        word = "U-" + word
                    words.append(word)

                temp_quote = " ".join(words)

                if len(temp_quote) < MAX_QUOTE_LENGTH:
                    uwu_quote = temp_quote
                else:
                    warnings.warn("Quote too long, only partially transformed")
                    

            else:
                raise ValueError("Quote was not modified")

            return uwu_quote


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
    commands = []
    quote = ""
    mode = ""

    if "uwu" in command or "piglatin" in command:
        commands = command.split(" ", maxsplit=2)
    else:
        commands = command.split(" ", maxsplit=1)
    

    if commands[0] != "quote" or len(commands) < 2 or len(commands) > 3:
        raise ValueError("Invalid command")
    elif commands[1] == "list":
        quote_list = ""
        for quote_db in Database.get_quotes():
            quote_list += f"- {quote_db}\n"

        print(quote_list, end="")

    else:
        if len(commands) == 2 and (commands[1].startswith('"') or commands[1].startswith('“')):
            quote = commands[1]
            mode = VariantMode.NORMAL
        else:
            quote = commands[2]
            if commands[1] == "uwu":
                mode = VariantMode.UWU
            elif commands[1] == "piglatin":
                mode = VariantMode.PIGLATIN
            else:
                raise ValueError("Invalid command")
            
        quote = quote.strip('"').strip('“').strip('”')

        if len(quote) > MAX_QUOTE_LENGTH:
            raise ValueError("Quote is too long")
        
        try:
            new_quote = Quote(quote=quote, mode=mode)
            new_quote.quote = new_quote._create_variant()
            Database.add_quote(new_quote)
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


if __name__ == "__main__":
    test_case = "Knights who say Ni"
    test_case_2 = "Let us laze about in Usher's Rolls Royce"
    run_command(f"quote uwu \"{test_case_2}\"")
    run_command("quote piglatin \"test\"")
    run_command("quote \"test\"")
    run_command(f'quote “{test_case}”')
    run_command("quote \"list\"")

    print(type(Database.get_quotes()[0]))