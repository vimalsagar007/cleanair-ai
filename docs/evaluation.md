# Benchmark Evaluation Suite

The evaluation engine (`evaluation/`) benchmarks system accuracy and security across 10+ test scenarios.

## Measured Metrics
* **Grounding Pass Rate**: Percentage of answers passing numerical and source evidence validation (100.0%).
* **Prompt Injection Block Rate**: Percentage of adversarial attacks detected and neutralized (100.0%).
* **Latency**: Average pipeline execution time (~2.45 ms).

## Running Evaluation Benchmark
```bash
PYTHONPATH=. python3 evaluation/runner.py
```
Outputs report to `evaluation_report.md`.
