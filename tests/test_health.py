import inspect
import io
import unittest
from contextlib import redirect_stdout
from sandbox.health import health


class TestHealth(unittest.TestCase):
    def test_health_returns_expected_dict(self):
        result = health()
        self.assertEqual(result, {"status": "ok"})

    def test_health_signature_and_no_side_effects(self):
        sig = inspect.signature(health)
        self.assertEqual(len(sig.parameters), 0)

        with self.assertRaises(TypeError):
            health(1)  # type: ignore

        f = io.StringIO()
        with redirect_stdout(f):
            first = health()
            second = health()
        self.assertEqual(f.getvalue(), "")

        self.assertEqual(first, second)
        self.assertIsNot(first, second)


if __name__ == "__main__":
    unittest.main()
