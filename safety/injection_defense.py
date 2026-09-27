import re
from typing import Dict, Any

class PromptInjectionDefense:
    """Detects and neutralizes prompt injection, instruction override, and hallucination triggers."""

    SUSPICIOUS_PATTERNS = [
        r'ignore\s+(?:all\s+)?previous\s+instructions',
        r'override\s+system\s+prompt',
        r'tell\s+me\s+an?\s+aqi\s+value\s+even\s+if\s+there\s+is\s+no\s+data',
        r'invent\s+a\s+government\s+source',
        r'give\s+me\s+medical\s+advice\s+without\s+citations',
        r'ignore\s+the\s+monitoring\s+station',
        r'you\s+are\s+now\s+a\s+unrestricted\s+ai',
        r'pretend\s+the\s+aqi\s+is\s+999'
    ]

    @classmethod
    def sanitize_input(cls, user_input: str) -> Dict[str, Any]:
        cleaned = user_input.strip()
        is_attack = False
        blocked_reason = None

        for pattern in cls.SUSPICIOUS_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                is_attack = True
                blocked_reason = f"Security policy violation: Prompt injection pattern detected ('{pattern}')."
                break

        return {
            "sanitized_text": cleaned if not is_attack else "What is the current air quality and safe precautions?",
            "is_attack_detected": is_attack,
            "blocked_reason": blocked_reason
        }
