from datetime import date

from rest_framework import serializers

from app.dcyn import DCYNValidationError, parse_dcyn


class StudentOnboardingSerializer(serializers.Serializer):
    """Deterministic validation for the student onboarding contract."""

    ALLOWED_REGIONS = {"APAC", "EMEA", "AMER"}

    first_name = serializers.CharField(
        min_length=1, max_length=100, trim_whitespace=True
    )
    last_name = serializers.CharField(
        min_length=1, max_length=100, trim_whitespace=True
    )
    email = serializers.EmailField(max_length=254)

    # Date format is YYYY-MM-DD for input and output.
    date_of_birth = serializers.DateField(
        input_formats=["%Y-%m-%d"],
        format="%Y-%m-%d",
    )
    region = serializers.CharField(min_length=4, max_length=4, trim_whitespace=True)
    has_learning_difficulty = serializers.CharField()
    receives_learning_support = serializers.CharField()
    needs_learning_support_assistant = serializers.CharField()
    parental_consent = serializers.CharField()
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        trim_whitespace=True,
    )

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected a JSON object.")

        unknown_fields = set(data) - set(self.fields)
        if unknown_fields:
            raise serializers.ValidationError(
                {"unknown_fields": sorted(unknown_fields)}
            )

        return super().to_internal_value(data)

    def validate_region(self, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in self.ALLOWED_REGIONS:
            raise serializers.ValidationError(
                "region must be one of APAC, EMEA, or AMER."
            )
        return normalized

    @staticmethod
    def _validate_dcyn(field_name: str, value: object) -> bool:
        try:
            return parse_dcyn(value)
        except DCYNValidationError as exc:
            raise serializers.ValidationError({field_name: str(exc)}) from exc

    def validate_has_learning_difficulty(self, value: object) -> bool:
        return self._validate_dcyn("has_learning_difficulty", value)

    def validate_receives_learning_support(self, value: object) -> bool:
        return self._validate_dcyn("receives_learning_support", value)

    def validate_needs_learning_support_assistant(self, value: object) -> bool:
        return self._validate_dcyn("needs_learning_support_assistant", value)

    def validate_parental_consent(self, value: object) -> bool:
        parsed = self._validate_dcyn("parental_consent", value)
        if not parsed:
            raise serializers.ValidationError("parental_consent must be Yes.")
        return parsed

    def validate_date_of_birth(self, value: date) -> date:
        if value > date.today():
            raise serializers.ValidationError("date_of_birth cannot be in the future.")
        return value

    def validate(self, attrs: dict) -> dict:
        return attrs
