import io
import sys
import unittest

import qualifier


class TestQuoteCreation(unittest.TestCase):

    def tearDown(self):
        qualifier.Database = Database
        qualifier.Database.quotes = []

    def test_normal_quote(self):
        test_cases = [
            "Hello World Hello World Hello World Hello World He",
            "Rubber Duck Debugging is best",
            "a"
        ]

        for test in test_cases:
            qualifier.run_command(f"quote \"{test}\"")
            self.assertEqual(str(qualifier.Database.quotes[-1]), test)

    def test_normal_too_long(self):
        test_case = "aaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

        with self.assertRaises(ValueError) as exc:
            qualifier.run_command(f'quote "{test_case}"')
        self.assertEqual("Quote is too long", str(exc.exception))

    def test_smart_quotes(self):
        test_case = "when life gives you lemons"
        qualifier.run_command(f'quote “{test_case}”')
        self.assertEqual(str(qualifier.Database.quotes[-1]), test_case)

    def test_uwu_quote(self):
        test_case = "Let us laze about in Usher's Rolls Royce"
        correct = "Wet u-us waze about in U-Ushew's Wowws Woyce"
        qualifier.run_command(f'quote uwu "{test_case}"')
        self.assertEqual(str(qualifier.Database.quotes[-1]), correct)

    def test_uwu_partial_convert(self):
        test_case = "It's time to d-d-d-d-d-d-d-d-d-d-d-duel unless..."
        correct = "It's time to d-d-d-d-d-d-d-d-d-d-d-duew unwess..."

        with self.assertWarns(Warning) as wrn:
            qualifier.run_command(f'quote uwu "{test_case}"')
            self.assertTrue(str(qualifier.Database.quotes[-1]) == correct)
        self.assertEqual("Quote too long, only partially transformed", str(wrn.warning))

    def test_uwu_too_long(self):
        test_case = "It's time to d-d-d-d-d-d-d-d-d-d-d-d-d-d-d-d-d-d-d-ance unless..."

        with self.assertRaises(ValueError) as exc:
            qualifier.run_command(f'quote uwu "{test_case}"')
        self.assertEqual("Quote is too long", str(exc.exception))

    def test_uwu_no_conversion(self):
        test_case = "sphinx of diamond, see me now"

        with self.assertRaises(ValueError) as exc:
            qualifier.run_command(f'quote uwu "{test_case}"')
        self.assertEqual("Quote was not modified", str(exc.exception))

    def test_piglatin_quote(self):
        test_case = "Invite our friends to brunch"
        correct = "Inviteway ourway iendsfray otay unchbray"

        qualifier.run_command(f'quote piglatin "{test_case}"')
        self.assertEqual(str(qualifier.Database.quotes[-1]), correct)

    def test_piglatin_quote_too_long(self):
        test_case = "Bubble Bubble Boiling Trouble Witches Brew and Something Something"
        with self.assertRaises(ValueError) as exc:
            qualifier.run_command(f'quote piglatin "{test_case}"')
        self.assertEqual("Quote is too long", str(exc.exception))

    def test_piglatin_no_conversion(self):
        test_case = "Perhaps it was a dark and stormy night"

        with self.assertRaises(ValueError) as exc:
            with self.assertWarns(Warning) as wrn:
                qualifier.run_command(f'quote piglatin "{test_case}"')
            self.assertEqual("Quote would be too long, was not piglatin-ified", str(wrn.warning))
        self.assertEqual("Quote was not modified", str(exc.exception))

    def test_do_nothing(self):
        test_case = "This sure looks like a quote"
        qualifier.run_command(f'uwu {test_case}')
        qualifier.run_command(f'piglatin {test_case}')
        qualifier.run_command(f'{test_case}')
        qualifier.run_command(f'quotes {test_case}')

        print(qualifier.Database.quotes)

        self.assertEqual(qualifier.Database.quotes, [])

    def test_database_error(self):
        test_case = "Hello World"
        qualifier.Database.quotes = [test_case]

        expected_output = "Quote has already been added previously\n"

        captured_ouput = io.StringIO()
        sys.stdout = captured_ouput

        qualifier.run_command(f'quote "{test_case}"')

        output = captured_ouput.getvalue()
        self.assertEqual(output, expected_output)

        sys.stdout = sys.__stdout__

    def test_display_quotes(self):
        quotes = [
            "Quote 1",
            "Quote 2 looks so sweet",
            "Quote 4 or wait... is it 3?"
        ]

        qualifier.Database.quotes = quotes

        correct = f"- {"\n- ".join(quotes)}\n"

        captured_ouput = io.StringIO()
        sys.stdout = captured_ouput

        qualifier.run_command("quote list")

        output = captured_ouput.getvalue()
        self.assertEqual(output, correct)

        sys.stdout = sys.__stdout__


class DuplicateError(Exception):
    ...


class Database:
    quotes = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return cls.quotes

    @classmethod
    def add_quote(cls, quote) -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in cls.quotes:
            raise DuplicateError
        cls.quotes.append(quote)


if __name__ == "__main__":
    unittest.main()
