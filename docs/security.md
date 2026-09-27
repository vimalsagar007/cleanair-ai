# Security, Guardrails & Prompt Injection Defense

CLEANAIR AI enforces enterprise security and safety guardrails:

## 1. Prompt Injection Defense
* **Pattern Filter**: Scans user inputs for instruction override attempts ("ignore previous instructions", "invent AQI 999", "override system prompt").
* **Neutralization**: Replaces hostile prompts with default safe queries while alerting the trace system.

## 2. Grounding Validation
* Verifies every numerical AQI claim against raw MCP tool data.
* Ensures health recommendations are backed by retrieved PDF contexts.
* Fails safely with *"Insufficient verified information to provide a reliable recommendation"* if grounding check fails.

## 3. Medical Disclaimers
* Non-diagnostic guardrail: Prohibits medical prescribing or diagnosis terminology.
