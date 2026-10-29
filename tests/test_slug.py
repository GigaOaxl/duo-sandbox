import unittest
from sandbox.slug import slug


class TestSlug(unittest.TestCase):
    def test_empty_string(self):
        """A-1: Leerer Text ergibt einen leeren String."""
        self.assertEqual(slug(""), "")

    def test_umlauts_and_sharp_s(self):
        """A-2: Umlaute werden zu ae, oe, ue, ss (ä->ae, ö->oe, ü->ue, ß->ss, Großbuchstaben Ä/Ö/Ü ebenso)."""
        self.assertEqual(slug("ä ö ü ß Ä Ö Ü"), "ae-oe-ue-ss-ae-oe-ue")
        self.assertEqual(slug("Größe & Übermaß!!"), "groesse-uebermass")

    def test_special_characters(self):
        """A-3: Sonderzeichen werden zu einem Bindestrich."""
        self.assertEqual(slug("hello world"), "hello-world")
        self.assertEqual(slug("hello@world!test"), "hello-world-test")

    def test_multiple_hyphens(self):
        """A-4: Mehrfache Bindestriche werden zu einem."""
        self.assertEqual(slug("foo---bar---baz"), "foo-bar-baz")
        self.assertEqual(slug("---foo---bar---"), "foo-bar")

    def test_max_length_100(self):
        """A-5: Ein Text mit 150 Zeichen ergibt höchstens 100 Zeichen."""
        long_text = "a" * 150
        result = slug(long_text)
        self.assertLessEqual(len(result), 100)
        self.assertEqual(len(result), 100)

        # Prüfen, dass nach dem Kürzen kein Bindestrich am Ende verbleibt
        trailing_dash_text = "a" * 99 + "-extra"
        trimmed_result = slug(trailing_dash_text)
        self.assertLessEqual(len(trimmed_result), 100)
        self.assertFalse(trimmed_result.endswith("-"))


if __name__ == "__main__":
    unittest.main()
