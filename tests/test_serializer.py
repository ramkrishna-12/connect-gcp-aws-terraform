
import unittest

from django.conf import settings

if not settings.configured:
    settings.configure(USE_I18N=False, SECRET_KEY="unit-test-only")

from app.dcyn import DCYNValidationError, parse_dcyn
from app.serializers import StudentOnboardingSerializer


VALID_PAYLOAD = {
    "first_name": "Maya",
    "last_name": "Sharma",
    "email": "maya.sharma@example.com",
    "date_of_birth": "2014-05-17",
    "region": "APAC",
    "has_learning_difficulty": "Yes",
    "receives_learning_support": "Yes",
    "needs_learning_support_assistant": "No",
    "parental_consent": "Yes",
    "notes": "Requires structured classroom support.",
}


class DCYNTests(unittest.TestCase):
    def test_yes_and_no_are_deterministic(self):
        self.assertTrue(parse_dcyn("Yes"))
        self.assertFalse(parse_dcyn("No"))
        self.assertTrue(parse_dcyn(" yes "))

    def test_unknown_value_is_rejected(self):
        with self.assertRaises(DCYNValidationError):
            parse_dcyn("Maybe")


class SerializerTests(unittest.TestCase):
    def test_valid_payload(self):
        serializer = StudentOnboardingSerializer(data=VALID_PAYLOAD)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.validated_data["parental_consent"])

    def test_invalid_dcyn_value(self):
        payload = {**VALID_PAYLOAD, "has_learning_difficulty": "Maybe"}
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("has_learning_difficulty", serializer.errors)

    def test_parental_consent_is_required(self):
        payload = {**VALID_PAYLOAD, "parental_consent": "No"}
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("parental_consent", serializer.errors)

    def test_unknown_fields_are_rejected(self):
        payload = {**VALID_PAYLOAD, "unexpected": "value"}
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("unknown_fields", serializer.errors)

    def test_notes_limit(self):
        payload = {**VALID_PAYLOAD, "notes": "x" * 501}
        serializer = StudentOnboardingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("notes", serializer.errors)


if __name__ == "__main__":
    unittest.main()
