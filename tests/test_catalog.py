import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check-catalog.py"
spec = importlib.util.spec_from_file_location("catalog", SCRIPT)
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = {"site": "sample-site", "environment": "test", "products": [{
            "sku": "credits-small", "name": "Credit pack", "type": "one_time",
            "amount": "5.25", "currency": "USD", "entitlement": "10 credits",
            "validity": "365 days", "refund_policy": "Review unused credits"}]}

    def test_valid_one_time(self):
        self.assertEqual(catalog.validate(self.data), [])

    def test_valid_subscription(self):
        self.data["products"][0].update(type="subscription", billing_period="Monthly")
        self.assertEqual(catalog.validate(self.data), [])

    def test_duplicate_sku(self):
        self.data["products"].append(copy.deepcopy(self.data["products"][0]))
        self.assertTrue(catalog.validate(self.data))

    def test_float_price(self):
        self.data["products"][0]["amount"] = 5.25
        self.assertTrue(catalog.validate(self.data))

    def test_invalid_prices(self):
        for amount in ("NaN", "Infinity", "-2", "0", "1e2", None):
            with self.subTest(amount=amount):
                self.data["products"][0]["amount"] = amount
                self.assertTrue(catalog.validate(self.data))

    def test_subscription_requires_cycle(self):
        self.data["products"][0]["type"] = "subscription"
        self.assertTrue(catalog.validate(self.data))

    def test_wrong_environment(self):
        self.data["environment"] = "live"
        self.assertTrue(catalog.validate(self.data))

    def test_credentials_rejected_without_echo(self):
        self.data["private_key"] = "SYNTHETIC_SECRET_MUST_NOT_APPEAR"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "catalog.json"
            path.write_text(json.dumps(self.data))
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(self.data["private_key"], result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
