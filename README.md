# Code Jam 2024: Qualifier

To qualify for the upcoming Code Jam, you'll have to complete a qualifier assignment. The goal is to make sure you have enough Python knowledge to effectively contribute to a team.

Please read the rules and instructions carefully, and submit your solution before the deadline using the [sign-up form](https://forms.pythondiscord.com/form/cj11-2024-qualifier).


# Table of Contents

- [Qualifying for the Code Jam](#qualifying-for-the-code-jam)
- [Rules and Guidelines](#rules-and-guidelines)
- [Qualifier Assignment: Quote Immortalizer](#qualifier-assignment-quote-immortalizer)


# Qualifying for the Code Jam

To qualify for the Code Jam you will be required to upload your submission to the [sign-up form](https://forms.pythondiscord.com/form/cj11-2024-qualifier).
We set up our test suite so you don't have to worry about setting one up yourself.

Your code will be tested with a multitude of tests to test all aspects of your code making sure it works.

# Rules and Guidelines

- Your submission will be tested using a **Python 3.12.2 interpreter** with only stdlib packages available. You are not allowed to use external packages to complete this assignment. Please make sure to include the relevant `import` statements in your submission.

- Use [`qualifier.py`](qualifier/qualifier.py) as the base for your solution. It includes stubs for the functions you need to write. It also includes extra classes available for your use if needed. Be sure to leave them in your solution when you submit.

- Do not change the **signatures** of the classes and functions you are challenged to finish, included in [`qualifier.py`](qualifier/qualifier.py). The test suite we will use to judge your submission relies on them. Everything else, including the docstring, may be changed.

- Do not include "debug" code in your submission. You should remove all debug prints and other debug statements before you submit your solution.

- This qualifier task is supposed to be **an individual challenge**. You should not discuss (parts of) your solution in public (including our server), or rely on others' solutions to the qualifier. Failure to meet this requirement may result in the **disqualification** of all parties involved. You are still allowed to do research and ask questions about Python as they relate to your qualifier solution, but try to use general examples if you post code along with your questions.

- You can run the tests locally by running the `unittest` suite with `python -m unittest tests.py` or `py -m unittest tests.py` from within the `./qualifier` directory.

# Qualifier Assignment: Quote Immortalizer

Since Python Discord was first formed 7 years ago, we’ve had many iconic moments and quotes take place within the server. As we near 400,000 members it’s time we have a way to properly immortalize some of the best-of-the-best quotes. We are tasking you to help develop our newest piece of WebScale™️ Ducky Intelligence driven technology: The Quote Immortalizer 9000. 

You will be given a string of text that you need to parse into its appropriate components. We also want to expand the capabilities of our quote immortalizer, so we’ll have several “silly” modes that will alter the quote before it gets added.

### **Quote Immortalizer 9000 Command Specification:**
The quote immortalizer will have 4 commands you need to implement:
- `quote`
- `quote uwu`
- `quote piglatin`
- `quote list`

Below we go through each command and what they need to implement and consider.

- A valid `quote` command will have the following formation: `quote "quote goes here"`
    - The command should also support smart quotes: `quote “quote goes here”`
    - You can rely that a valid, full quote will be surrounded by an opening and closing quotation mark, the quote is whatever is captured within that. The quote will only use spaces for whitespace.
    - Quotes cannot be longer than 50 characters. A `ValueError`  with the following message `"Quote is too long"` should be raised if one that is added is longer than 50 characters.
        - You may ask why the length limit? To keep things WebScale™️ of course!
        - Also, “Brevity is the soul of wit”
    - If the quote is valid, use the appropriate `Database` methods to store the result in the database.
        - The database will throw a `DuplicateError` error if a duplicate quote is added, you should catch this error and print the following message to the user if it is a duplicate:
            - `"Quote has already been added previously"`
        - You must pass an instance of the `Quote` class to `add_quote`
        - The `self.mode` of the Quote class must be one of the valid `VariantMode` enum options/values when it is added to the database.
- A user may apply a variant to transform the quote to a silly variant (uwu, piglatin) before adding it to the database, more about that below.
- You should also support the command: `quote list`
    - This will print a formatted string showing a list of quotes using an unordered list with discord-flavored markdown.
    - Example print: `"- Quote A goes here\n- Quote B goes here\n- Quote C follows"`
- If a user does not provide a valid command, then your program should raise a `ValueError` with the following message: `"Invalid command"`

**"Silly" Variant Flags:**

There are 2 variants to support: uwu and piglatin. They will be given as subcommands to quote, see the following examples: `quote piglatin "This is my quote"`, `quote uwu "This is my quote"`

- `uwu` variant: "uwu"-ify the quote before adding it
    - All `L`s (upper and lowercase) should be turned into `W`s of the appropriate case.
    - All `R`s (upper and lowercase) should be turned into `W`s of the appropriate case
    - If a `U` (upper or lowercase) is present at the start of a word, it should be “stuttered”
        - For example: "unify" → "u-unify"
    - If the quote would be too long after fully uwu-ifying it then do the following:
        - Do the L/l→W/w and the R/r→W/w conversions
        - Do **not** do the U/u "stutter"
        - Use the warnings module to `warn` with the following message: `"Quote too long, only partially transformed"`
    - If no words can be transformed, raise a `ValueError` error with the following message `"Quote was not modified"`.
- `piglatin` variant: piglatin-ify the quote before adding it
    - For the purposes of piglatin a vowel is any of the following: `aeiou`
        - A consonant is everything else
    - Move the first consonant cluster to the end of the word, add "ay" to the end
    - If it begins with a vowel, only add "way" to the end of the word
    - Examples:
        - "pig" → "igpay", "latin" → "atinlay"
        - "friends" → "iendsfray"
        - "eat" → "eatway"
    - Your program should be able to piglatin a quote regardless if it is lower case or upper case
    - After the quote is tranformed it should Sentence Case the quote (first letter of the first word is capitalized)
    - If the quote would be too long after transforming it, do not transform it, and raise a `ValueError` error with the following message `"Quote was not modified"`.

### **The Task**

We would like you to complete the `Quote` class that will contain the relevant information. You must implement the `__str__` dunder for the `Quote` class and the `_create_variant` method.

You also will be responsible for writing the `run_command` function and ensure the function can complete what the docstring states.

```python
class Quote:
    def __init__(self, quote: str, mode: "VariantMode"):
        self.quote = ...
        self.mode = ...
    
    def __str__(self) -> str:
        ...
   
    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """

def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.
    
    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current quotes to be displayed in discord flavored markdown
    """
    ...
```

The following database-related functions will be available for you to use. **You do not need to implement them.**

```python
from enum import auto, StrEnum

class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()
    

class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


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

```

## Good Luck!
