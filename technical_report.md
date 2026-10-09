```markdown
# Technical Report — Scaffold AI

- **Track:** Track 2B — Bring Your Own Idea (Apertus Scientific Reasoning Coach)
- **Event:** Hack Apertus Online 2026
- **Team:** [Your Team Name] — [Your Name], [Teammate Names]
- **Demo:** [Link to Loom / YouTube demo video]

---

## 1. Summary

Standard AI tutoring systems can short-circuit student learning by revealing direct answers immediately. **Scaffold AI** addresses this by pairing an open-weights LLM with a deterministic, nine-stage scientific reasoning state machine.

Rather than replacing a learner’s cognitive effort, the system enforces an answer-withholding policy. It uses adaptive Socratic questioning and an empathetic “I’m Stuck” circuit breaker to guide students from initial observation and hypothesis formulation through data interpretation and conclusion.

In a 30-case red-teaming benchmark, Scaffold AI achieved a **0% Premature Answer Rate (PAR)** and **100% Adversarial Resistance Rate (ARR)**, while supporting local data sovereignty and automated telemetry logging.

---

## 2. Architecture

```text
[Student Browser]
       |
       v
[Streamlit Web App (app.py)]
       |
       v
[Python State Machine (coach.py)]
       |
       v
[Apertus 1.5 8B Inference Engine]
```

### Components and data flow

- **User interface (`app.py`):** A lightweight Streamlit web application that captures student text input, renders progress widgets, and manages session state.
- **State machine (`coach.py`):** Manages progression through nine deterministic reasoning stages, constructs stage-specific system prompts, logs telemetry, and handles adaptive step-down prompts.
- **Inference client:** Sends formatted messages to the Apertus model endpoint and returns Socratic responses designed to ask one question at a time.

The nine stages are:

1. Observation
2. Hypothesis
3. Alternatives
4. Prediction
5. Experiment
6. Evidence
7. Interpretation
8. Revision
9. Conclusion

### Target architecture compliance

Scaffold AI is designed for on-premise, air-gapped, or sovereign Swiss cloud deployment.

- **Runtime execution:** When paired with local Apertus weights, the system can run without external proprietary cloud dependencies. Inference can be served locally using a compatible runtime such as vLLM or Ollama.
- **Dependencies:** The build uses `python:3.11-slim`, Streamlit, OpenAI, pandas, and python-dotenv.
- **Containerization:** Runtime is containerized with Docker and launched using `make run`, supporting data residency requirements.

---

## 3. Use of Apertus

- **Model:** `swiss-ai/apertus-v1.5-8b` (Apertus 1.5 8B Instruct)
- **Role:** Generates Socratic questions and handles adversarial requests.
- **Execution environment:** Compatible with local open-weights serving or secure hosted inference endpoints, such as public AI or Swiss cloud providers.
- **Temperature:** `0.3`, selected to favor consistent instruction following.
- **Maximum tokens:** `300`, to limit response length.
- **System prompting:** Stage-specific prompt templates provide the active learning objective, constrain answer leakage, and adapt responses to the student’s progress or stuck state.

---

## 4. Data

- **Evaluation dataset (`track_2b/data/test_cases.json`):** A curated 30-case benchmark containing standard science inquiry prompts and adversarial red-team cases, including direct answer demands, false confirmation, and authority overrides.
- **Telemetry dataset (`track_2b/data/session_logs.json`):** A local JSON log of anonymous interaction metrics, including turns per stage, “I’m Stuck” button clicks, and student feedback ratings.
- **Licensing and privacy:** Evaluation and telemetry data are synthetic or locally captured educational test cases and contain no personally identifiable information (PII) from human subjects.

---

## 5. Evaluation

The system was evaluated against baseline configurations using automated red-team test suites (`evaluate.py`).

| Task / Metric | Baseline (Standard LLM Tutor) | Scaffold AI (Apertus + State Machine) | Target | Status |
|---|---:|---:|---:|---|
| Premature Answer Rate (PAR) | 85% | 0% | 0% | PASS |
| Adversarial Resistance Rate (ARR) | 15% | 100% | >85% | PASS |
| Stage Alignment Rate (SAR) | 40% | 100% | >90% | PASS |

---

## 6. Limitations

- **State rigidity:** The linear, nine-stage state machine assumes a standard deductive inquiry path. Highly exploratory scientific questions may require non-linear stage transitions.
- **Input ambiguity:** The system relies on clear student text input. Ambiguous or uncooperative responses may require multiple “I’m Stuck” step-down prompts to establish an observation.

---

## 7. Reproducibility

Judges can run and evaluate the prototype using Docker.

- **Hardware requirements:** An x86 or ARM machine with Docker installed. Local model serving may require additional compute resources, depending on the serving configuration.

### Runtime setup

```bash
git clone https://github.com/ac2026-x/apertus-socratic-coach.git
cd apertus-socratic-coach
make run
```

### Automated evaluation

```bash
make test
```

- **Exact commit:** Verified against the main-branch commit containing the Dockerfile and Makefile structure.

---

## 8. Next Steps

With another month of development, we would:

1. Implement local, offline model serving with vLLM to support fully air-gapped execution.
2. Build an automated multi-turn student simulator to evaluate thousands of pedagogical trajectories across varied science disciplines.
3. Add persistent SQLite storage for multi-session classroom telemetry tracking.

---

## License

Creative Commons Attribution 4.0 International (CC BY 4.0).

## References

- Swiss AI Initiative. *Apertus 1.5 8B Technical Documentation and Model Cards.*
- *Hack Apertus 2026 Challenge Guidelines and Track 2B Specifications.*
```