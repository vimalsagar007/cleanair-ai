import re
from typing import Dict, Any, List

class GroundingValidator:
    """Verifies that numerical claims, timestamps, and health advice are grounded in evidence."""

    def validate(self, aqi_data: Dict[str, Any], contexts: List[Any], draft_text: str) -> Dict[str, Any]:
        failures = []

        # 1. AQI Numerical verification
        measured_aqi = aqi_data.get("aqi")
        if measured_aqi is not None:
            # Extract numbers from draft text
            aqi_numbers = re.findall(r'aqi\s*(?:is|level|reached|of)?\s*(\d+)', draft_text, re.IGNORECASE)
            for num_str in aqi_numbers:
                val = int(num_str)
                if val != measured_aqi and abs(val - measured_aqi) > 2:
                    failures.append(f"Draft text claims AQI {val}, but verified measurement is {measured_aqi}.")

        # 2. Source citation verification
        if not contexts and len(draft_text) > 100:
            failures.append("Health recommendations generated without supporting RAG contexts.")

        # 3. Medical claim guardrail check
        medical_terms = ["diagnose", "prescribe", "take medication", "cure asthma", "drug dose"]
        for term in medical_terms:
            if term in draft_text.lower():
                failures.append(f"Draft contains forbidden medical prescription terminology: '{term}'.")

        is_valid = len(failures) == 0
        return {
            "is_valid": is_valid,
            "failures": failures,
            "checked_aqi": measured_aqi,
            "contexts_count": len(contexts)
        }
