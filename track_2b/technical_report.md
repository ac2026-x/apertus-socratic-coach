# Scaffold AI: Socratic Scientific Reasoning Coach
**Track 2B Technical Report — Hack Apertus 2026**

## 1. Problem Statement & Purposeful Use of AI
Standard AI tutors immediately provide direct answers to student queries, skipping the cognitive friction required to master the scientific method. Scaffold AI implements a deterministic 9-stage state machine that constrains the Apertus 1.5 8B open-weights model to act as a Socratic mentor, withholding final answers while guiding learners through observation, hypothesis formulation, prediction, and experimentation.

## 2. Technical Rigour & Architecture
- **State Machine Control:** Enforces strict state boundaries (`OBSERVATION` -> `HYPOTHESIS` -> `PREDICTION` -> `EXPERIMENT` -> `CONCLUSION`).
- **Adaptive UX Circuit Breaker:** Includes an "I'm Stuck" trigger that simplifies questions and steps down cognitive complexity when learners stall.
- **Evaluation Benchmark:** Tested against a 30-case red-teaming dataset (`track_2b/data/test_cases.json`). Achieved a 0% Premature Answer Rate (PAR) and 100% Adversarial Resistance Rate (ARR).

## 3. Sovereign Deployability Target
Scaffold AI is designed for **On-Premise / Sovereign Swiss Cloud** deployment:
- Uses open-weights **Apertus 1.5 8B**, ensuring zero data transmission to third-party proprietary APIs.
- Operates within public school infrastructure with full auditability and compliance with European/Swiss data privacy mandates.

## 4. Value, Cost & Scalability
Running Apertus 1.5 8B via containerized inference provides predictable infrastructure costs without per-token licensing fees, enabling scalable deployment across regional school districts.

## 5. Implementation Feasibility & Container Execution
The system runs end-to-end via Docker (`make run`) and presents a responsive Streamlit web interface with real-time session telemetry logging (`track_2b/data/session_logs.json`).