import unittest
from sanitize import scrub_pii

class TestSanitize(unittest.TestCase):
    def test_email_removal(self):
        text = "Contact me at user@example.com for more info."
        expected = "Contact me at [EMAIL REDACTED] for more info."
        self.assertEqual(scrub_pii(text), expected)

    def test_phone_removal(self):
        text = "Call +1-800-555-1234 to get help."
        expected = "Call [PHONE REDACTED] to get help."
        self.assertEqual(scrub_pii(text), expected)

    def test_id_removal(self):
        text = "My transaction ID is XA9B3KF892L."
        expected = "My transaction ID is [ID REDACTED]."
        self.assertEqual(scrub_pii(text), expected)

    def test_clean_text(self):
        text = "This app is great, I love using it!"
        self.assertEqual(scrub_pii(text), text)

if __name__ == '__main__':
    unittest.main()
