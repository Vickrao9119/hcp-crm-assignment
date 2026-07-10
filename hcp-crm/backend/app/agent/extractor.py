"""
Rule-based fallback entity extractor.

Used when no GROQ_API_KEY is configured, so the AI Chat feature still works
out of the box in local/dev environments. When a key is present, the
LangGraph agent (graph.py) calls Groq's Gemma2-9B-IT for higher quality
extraction and this module is unused.
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

PRIORITY_KEYWORDS = {
    "high": ["urgent", "asap", "high priority", "immediately", "critical"],
    "low": ["low priority", "no rush", "whenever"],
}


def _next_weekday(day_name: str) -> datetime:
    today = datetime.utcnow()
    target = WEEKDAYS.index(day_name.lower())
    days_ahead = (target - today.weekday() + 7) % 7
    days_ahead = days_ahead or 7
    return today + timedelta(days=days_ahead)


def extract_entities(text: str) -> Dict[str, Any]:
    """Extract doctor, hospital, products, priority, and follow-up date from free text."""
    entities: Dict[str, Any] = {
        "doctor": None,
        "hospital": None,
        "products": [],
        "priority": "medium",
        "follow_up_date": None,
        "samples_requested": False,
    }

    doctor_match = re.search(r"Dr\.?\s+([A-Z][a-zA-Z]+)", text)
    if doctor_match:
        entities["doctor"] = f"Dr. {doctor_match.group(1)}"

    hospital_match = re.search(
        r"at\s+([A-Z][A-Za-z\s]+?(?:Hospital|Clinic|Medical Center|Institute))", text
    )
    if hospital_match:
        entities["hospital"] = hospital_match.group(1).strip()

    product_keywords = re.findall(
        r"\b(diabetes|cardiac|insulin|antibiotic[s]?|pain relief|vitamins?|"
        r"[A-Z][a-z]+(?:mycin|cillin|statin|prazole))\b",
        text,
        re.IGNORECASE,
    )
    entities["products"] = list({p.strip().title() for p in product_keywords})

    lowered = text.lower()
    if "sample" in lowered:
        entities["samples_requested"] = True

    for level, keywords in PRIORITY_KEYWORDS.items():
        if any(k in lowered for k in keywords):
            entities["priority"] = level

    for day in WEEKDAYS:
        if day in lowered:
            entities["follow_up_date"] = _next_weekday(day).isoformat()
            break

    return entities


def summarize(text: str, entities: Dict[str, Any]) -> str:
    """Produce a short human-readable summary from the raw text and extracted entities."""
    parts = []
    if entities.get("doctor"):
        parts.append(f"Met with {entities['doctor']}")
    if entities.get("hospital"):
        parts.append(f"at {entities['hospital']}")
    if entities.get("products"):
        parts.append(f"discussing {', '.join(entities['products'])}")
    summary = " ".join(parts) if parts else text[:120]
    if entities.get("samples_requested"):
        summary += ". Samples were requested."
    if entities.get("follow_up_date"):
        summary += f" Follow-up scheduled."
    return summary.strip()
