from typing import Dict, Any, List
from safety.grounding import GroundingValidator

class EvidenceAgent:
    """Agent responsible for grounding validation, source checking, and numerical verification."""

    def __init__(self):
        self.validator = GroundingValidator()

    async def validate_evidence(self, aqi_data: Dict[str, Any], health_contexts: List[Any], draft_response: str) -> Dict[str, Any]:
        validation_result = self.validator.validate(
            aqi_data=aqi_data,
            contexts=health_contexts,
            draft_text=draft_response
        )
        return validation_result
