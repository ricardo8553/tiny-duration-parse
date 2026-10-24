import unittest

from tiny_duration_parse import parse, render, ParseError


class TestParse(unittest.TestCase):
    def test_single_seconds(self):
        self.assertEqual(parse("30s"), {"s": 30})

    def test_hours_minutes(self):
        self.assertEqual(parse("2h30m"), {"h": 2, "m": 30})

    def test_milliseconds(self):
        self.assertEqual(parse("500ms"), {"ms": 500})

    def test_days(self):
        self.assertEqual(parse("1d"), {"d": 1})

    def test_all_units(self):
        self.assertEqual(
            parse("1d2h3m4s5ms"),
            {"d": 1, "h": 2, "m": 3, "s": 4, "ms": 5},
        )

    def test_reversed_order_preserved(self):
        self.assertEqual(parse("5ms4s3m2h1d"), {"ms": 5, "s": 4, "m": 3, "h": 2, "d": 1})

    def test_empty_raises(self):
        with self.assertRaises(ParseError):
            parse("")

    def test_whitespace_rejected(self):
        with self.assertRaises(ParseError):
            parse("2h 30m")

    def test_leading_whitespace_rejected(self):
        with self.assertRaises(ParseError):
            parse(" 2h30m")

    def test_uppercase_rejected(self):
        with self.assertRaises(ParseError):
            parse("2H30M")

    def test_unknown_unit_rejected(self):
        with self.assertRaises(ParseError):
            parse("2y")

    def test_duplicate_unit_rejected(self):
        with self.assertRaises(ParseError):
            parse("2h3h")

    def test_non_string_rejected(self):
        with self.assertRaises(ParseError):
            parse(123)


class TestRender(unittest.TestCase):
    def test_roundtrip_simple(self):
        self.assertEqual(render(parse("2h30m")), "2h30m")

    def test_canonical_ordering(self):
        self.assertEqual(render({"m": 30, "h": 2}), "2h30m")

    def test_zero_components_omitted(self):
        self.assertEqual(render({"h": 2, "m": 0, "s": 0}), "2h")

    def test_all_zero(self):
        self.assertEqual(render({"s": 0}), "0s")

    def test_empty_dict(self):
        self.assertEqual(render({}), "0s")

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            render({"s": -1})


class TestRoundTrip(unittest.TestCase):
    def test_complex_roundtrip(self):
        s = "1d2h3m4s5ms"
        self.assertEqual(render(parse(s)), s)

    def test_render_then_parse(self):
        parts = {"h": 1, "m": 30}
        rendered = render(parts)
        self.assertEqual(parse(rendered), parts)


if __name__ == "__main__":
    unittest.main()
