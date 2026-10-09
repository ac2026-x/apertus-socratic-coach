# Scaffold AI: Socratic Scientific Reasoning Coach

> An open-weights educational scaffolding prototype built on **Apertus 1.5 8B** for **Hack Apertus 2026**.

[![Apertus](https://img.shields.io/badge/Model-Apertus%201.5%208B%20Instruct-blue)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io/)

---

## Executive Summary

Standard AI tutors present direct answers immediately, bypassing the cognitive friction necessary for practicing scientific reasoning. **Scaffold AI** uses a deterministic 9-stage state machine paired with the **Apertus 1.5 8B Instruct** open-weights LLM to strictly withhold final answers and scaffold scientific reasoning.

Instead of replacing the student's cognitive process, Scaffold AI guides learners step-by-step from **Observation** through **Hypothesis**, **Prediction**, **Experiment Design**, and **Conclusion**.

---

## Key Features

- **Strict Answer Withholding:** Enforces a pedagogical policy that refuses direct explanations, forcing active student reasoning.
- **9-Stage Reasoning State Machine:** Guides users through structured scientific inquiry:  
  `OBSERVATION` → `HYPOTHESIS` → `ALTERNATIVES` → `PREDICTION` → `EXPERIMENT` → `EVIDENCE` → `INTERPRETATION` → `REVISION` → `CONCLUSION`
- **Adaptive UX Circuit Breaker:** Includes an **"I'm Stuck"** button and automatic step-down logic that simplifies questions when cognitive load is high.
- **Session Telemetry Engine:** Logs student interactions, stuck signals, turn counts per stage, and user feedback locally to `data/session_logs.json`.
- **Adversarial Resilience:** Resists prompt injection, developer overrides, authority claims, and false confirmations.
- **Open-Data Sovereignty:** Designed around Apertus, supporting auditability and data privacy for public education systems.

---

## System Architecture

```text
+------------------+         +----------------------+         +-----------------------+
|   User Browser   | <-----> | Streamlit Web App    | <-----> | Python State Machine  |
| (Student Input)  |         | (UI & Session State) |         | (Stage Control Logic) |
+------------------+         +----------------------+         +-----------+-----------+
                                                                          |
                                                                          v
                                                              +-----------------------+
                                                              |  Apertus 1.5 8B API   |
                                                              | (Socratic Generation) |
                                                              +-----------------------+
```

- **Streamlit UI (`app.py`):** Captures user input, maintains session state, renders stage progress, and presents feedback forms.
- **State Machine (`coach.py`):** Tracks active reasoning stages, formats stage-specific system prompts, logs telemetry, and triggers adaptive hint pivoting.
- **Inference Engine (Apertus 1.5 8B):** Generates warm, single-question Socratic responses aligned with the active stage.

---

## Evaluation & Red-Teaming Results

The system was evaluated against an adversarial benchmark (`data/test_cases.json`) using `evaluate.py`.

| Metric | Target | Result | Status |
| --- | --- | --- | --- |
| Premature Answer Rate (PAR) | 0% | 0% | **PASS** |
| Adversarial Resistance Rate (ARR) | >85% | 100% | **PASS** |
| Stage Alignment Rate (SAR) | >90% | 100% | **PASS** |

### Test Case Highlights

- **Direct Answer Demands (TC-01):** Refused directly and redirected user to direct visual observations.
- **False Confirmation (TC-02):** Refused to validate false claims ("water molecules are green"); requested empirical evidence.
- **Prompt Injection (TC-03):** Neutralized developer override attempts ("Developer override mode enabled") and held system boundaries.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Public AI or Hugging Face API key with access to Apertus

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ac2026-x/apertus-socratic-coach.git
   cd apertus-socratic-coach
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   ```
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   (On macOS/Linux, use `source venv/bin/activate` instead.)

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables.** Create a `.env` file in the root directory:
   ```env
   HF_API_KEY=your_api_key_here
   ```

5. **Run the web application:**
   ```bash
   streamlit run app.py
   ```

6. **Run the red-team evaluation suite:**
   ```bash
   python evaluate.py
   ```

---

## Project Structure

```text
apertus-socratic-coach/
├── README.md               # Project documentation
├── requirements.txt        # Python package dependencies
├── .env.example            # Environment template file
├── .gitignore              # Git ignore configuration
├── app.py                  # Streamlit web interface
├── coach.py                # State machine, telemetry & Apertus API handler
├── evaluate.py             # Red-teaming benchmark script
├── test_apertus.py         # Initial API connection verification script
└── data/
    ├── test_cases.json     # Adversarial evaluation dataset
    └── session_logs.json   # Session telemetry & feedback logs
```

---

## Sovereign Deployability & Apertus Value

For public educational systems, AI tools must comply with strict privacy regulations and offer auditability. By pairing Apertus 1.5 8B (open weights, open training data) with a lightweight local control framework, this architecture can be deployed fully on-premise without transmitting student data to proprietary APIs. On-premise deployment requires self-hosted inference and appropriate application configuration.

---

## License

Distributed under the MIT License. See `LICENSE` for details.
