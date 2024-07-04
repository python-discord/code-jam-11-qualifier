import io
import sys
import unittest

import qualifier


class TestQuoteCreation(unittest.TestCase):

    def setUp(self):
        qualifier.Database.quotes = []

    def test_normal_quote(self):
        test_cases = [
            "Help! Help! I'm being repressed",
            "That rabbit's dynamite",
            "A scratch?"
        ]

        for test in test_cases:
            with self.subTest(test=test):
                qualifier.run_command(f"quote \"{test}\"")
                self.assertEqual(str(qualifier.Database.quotes[-1]), test)

    def test_normal_too_long(self):
        test_case = "aaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

        with self.assertRaises(ValueError) as exc:
            qualifier.run_command(f'quote "{test_case}"')
        self.assertEqual("Quote is too long", str(exc.exception))

    def test_smart_quotes(self):
        test_case = "Knights who say Ni"
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
        test_case = "Sphinx of diamond, see me now"

        with self.assertRaises(ValueError) as exc:
            qualifier.run_command(f'quote uwu "{test_case}"')
        self.assertEqual("Quote was not modified", str(exc.exception))

    def test_piglatin_quote(self):
        test_case = "Tis but a scratch"
        correct = "Istay utbay away atchscray"

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
            qualifier.run_command(f'quote piglatin "{test_case}"')
        self.assertEqual("Quote was not modified", str(exc.exception))

    def test_invalid_command(self):
        test_case = "This sure looks like a quote"
        invalid_commands = [
            f'uwu {test_case}',
            f'piglatin {test_case}',
            test_case,
            f'quotes {test_case}'
        ]

        for command in invalid_commands:
            with self.subTest(command=command):
                with self.assertRaises(ValueError) as exc:
                    qualifier.run_command(command)
                self.assertEqual("Invalid command", str(exc.exception))

    def test_database_error(self):
        test_case = "African or European swallow?"
        qualifier.Database.quotes = [test_case]

        expected_output = "Quote has already been added previously\n"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        qualifier.run_command(f'quote "{test_case}"')

        output = captured_output.getvalue()
        self.assertEqual(output, expected_output)

        sys.stdout = sys.__stdout__

    def test_database_error_quote(self):
        test_case = 'Nobody expects the Spanish Inquisition!'

        expected_output = "Quote has already been added previously\n"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        qualifier.run_command(f'quote "{test_case}"')
        qualifier.run_command(f'quote "{test_case}"')

        output = captured_output.getvalue()
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

        captured_output = io.StringIO()
        sys.stdout = captured_output

        qualifier.run_command("quote list")

        output = captured_output.getvalue()
        self.assertEqual(output, correct)

        sys.stdout = sys.__stdout__

    def test_quote_instance(self):
        test_case = 'Nobody expects the Spanish Inquisition!'
        qualifier.run_command(f'quote "{test_case}"')

        self.assertIsInstance(qualifier.Database.quotes[-1], qualifier.Quote)

    def test_variant_attribute(self):
        test_case = 'Tis but a scratch'
        qualifier.run_command(f'quote uwu "{test_case}"')

        added_quote = qualifier.Database.quotes[-1]
        self.assertIsInstance(added_quote.mode, qualifier.VariantMode)
        self.assertEqual(added_quote.mode, "uwu")

    def test_create_variant_implemented(self):
        quote_str = "Code golfers beware"
        test_cases = (
            (qualifier.VariantMode.NORMAL, "Code golfers beware"),
            (qualifier.VariantMode.UWU, "Code gowfews bewawe"),
            (qualifier.VariantMode.PIGLATIN, "Odecay olfersgay ewarebay")
        )

        self.assertTrue(hasattr(qualifier.Quote, '_create_variant'))

        for mode, variant_result in test_cases:
            quote = qualifier.Quote(quote_str, qualifier.VariantMode.NORMAL)
            with self.subTest(mode=mode, variant_result=variant_result):
                quote.mode = mode
                self.assertEqual(quote._create_variant(), variant_result)


if __name__ == "__main__":
    unittest.main()
