"""Unit tests for the rule-based fallback entity extractor."""
from datetime import datetime

import pytest

from app.agent import extractor


class TestNextWeekday:
    def test_returns_future_date(self):
        result = extractor._next_weekday("monday")
        assert result > datetime.utcnow()

    def test_lands_on_requested_weekday(self):
        for day_index, day_name in enumerate(extractor.WEEKDAYS):
            result = extractor._next_weekday(day_name)
            assert result.weekday() == day_index

    def test_is_case_insensitive(self):
        assert extractor._next_weekday("MONDAY").weekday() == 0

    def test_never_returns_today_when_same_weekday(self):
        today_name = extractor.WEEKDAYS[datetime.utcnow().weekday()]
        result = extractor._next_weekday(today_name)
        # days_ahead is forced to 7 when it would otherwise be 0
        assert (result - datetime.utcnow()).days >= 6

    def test_unknown_weekday_raises(self):
        with pytest.raises(ValueError):
            extractor._next_weekday("someday")


class TestExtractEntities:
    def test_empty_text_returns_defaults(self):
        entities = extractor.extract_entities("")
        assert entities == {
            "doctor": None,
            "hospital": None,
            "products": [],
            "priority": "medium",
            "follow_up_date": None,
            "samples_requested": False,
        }

    def test_extracts_doctor_with_period(self):
        assert extractor.extract_entities("Met Dr. Sharma today")["doctor"] == "Dr. Sharma"

    def test_extracts_doctor_without_period(self):
        assert extractor.extract_entities("Met Dr Gupta today")["doctor"] == "Dr. Gupta"

    def test_no_doctor_when_absent(self):
        assert extractor.extract_entities("Visited the clinic")["doctor"] is None

    def test_extracts_hospital(self):
        entities = extractor.extract_entities("Visited at Apollo Hospital yesterday")
        assert entities["hospital"] == "Apollo Hospital"

    def test_extracts_clinic_and_strips_whitespace(self):
        entities = extractor.extract_entities("Consultation at Sunrise Clinic went well")
        assert entities["hospital"] == "Sunrise Clinic"

    def test_extracts_known_product_keywords(self):
        products = extractor.extract_entities("Discussed diabetes and insulin options")["products"]
        assert set(products) == {"Diabetes", "Insulin"}

    def test_extracts_suffix_based_products(self):
        products = extractor.extract_entities("Prescribed Amoxicillin and Omeprazole")["products"]
        assert "Amoxicillin" in products
        assert "Omeprazole" in products

    def test_products_are_deduplicated(self):
        products = extractor.extract_entities("insulin insulin insulin")["products"]
        assert products == ["Insulin"]

    def test_samples_requested_flag(self):
        assert extractor.extract_entities("Doctor requested free samples")["samples_requested"] is True

    def test_samples_not_requested_by_default(self):
        assert extractor.extract_entities("Routine visit")["samples_requested"] is False

    def test_high_priority_keywords(self):
        assert extractor.extract_entities("This is urgent")["priority"] == "high"

    def test_low_priority_keywords(self):
        assert extractor.extract_entities("no rush on this one")["priority"] == "low"

    def test_default_priority_is_medium(self):
        assert extractor.extract_entities("A normal note")["priority"] == "medium"

    def test_follow_up_date_from_weekday(self):
        entities = extractor.extract_entities("Follow up next monday please")
        assert entities["follow_up_date"] is not None
        parsed = datetime.fromisoformat(entities["follow_up_date"])
        assert parsed.weekday() == 0

    def test_no_follow_up_date_without_weekday(self):
        assert extractor.extract_entities("Follow up soon")["follow_up_date"] is None

    def test_full_sentence_integration(self):
        text = (
            "Today I visited Dr. Sharma at Apollo Hospital, discussed diabetes "
            "medicines, doctor requested samples, urgent follow up next friday."
        )
        entities = extractor.extract_entities(text)
        assert entities["doctor"] == "Dr. Sharma"
        assert entities["hospital"] == "Apollo Hospital"
        assert "Diabetes" in entities["products"]
        assert entities["samples_requested"] is True
        assert entities["priority"] == "high"
        assert datetime.fromisoformat(entities["follow_up_date"]).weekday() == 4


class TestSummarize:
    def test_full_summary(self):
        entities = {
            "doctor": "Dr. Sharma",
            "hospital": "Apollo Hospital",
            "products": ["Insulin", "Diabetes"],
            "samples_requested": True,
            "follow_up_date": "2026-01-01T00:00:00",
        }
        summary = extractor.summarize("raw text", entities)
        assert "Met with Dr. Sharma" in summary
        assert "at Apollo Hospital" in summary
        assert "discussing Insulin, Diabetes" in summary
        assert "Samples were requested." in summary
        assert "Follow-up scheduled." in summary

    def test_falls_back_to_truncated_text_when_no_entities(self):
        text = "x" * 200
        summary = extractor.summarize(text, {})
        assert summary == "x" * 120

    def test_samples_appended_even_without_parts(self):
        summary = extractor.summarize("note", {"samples_requested": True})
        assert summary.endswith("Samples were requested.")

    def test_only_doctor(self):
        summary = extractor.summarize("note", {"doctor": "Dr. Lee"})
        assert summary == "Met with Dr. Lee"
