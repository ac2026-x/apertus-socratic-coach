# Scaffold AI: Socratic Scientific Reasoning Coach

> An open-weights educational scaffolding prototype built on **Apertus 1.5 8B** for **Hack Apertus 2026**.

[![Apertus](https://img.shields.io/badge/Model-Apertus%201.5%208B%20Instruct-blue)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io/)

---

## Executive Summary

Standard AI tutors present direct answers immediately, bypassing the cognitive friction necessary for practicing the scientific reasoning. **Scaffold AI** uses a deterministic 9-stage state machine paired with the **Apertus 1.5 8B Instruct** open-weights LLM to strictly withhold final answers and scaffold scientific reasoning.

Instead of replacing the student's cognitive process, Scaffold AI guides learners step-by-step from **Observation** through **Hypothesis**, **Prediction**, **Experiment Design**, and **Conclusion**.

---

## Key Features

- **Strict Answer Withholding:** Enforces a pedagogical policy that refuses direct explanations, forcing active student reasoning.
- **9-Stage Reasoning State Machine:** Guides users through structured scientific inquiry:
  `OBSERVATION` $\rightarrow$ `HYPOTHESIS` $\rightarrow$ `ALTERNATIVES` $\rightarrow$ `PREDICTION` $\rightarrow$ `EXPERIMENT` $\rightarrow$ `EVIDENCE` $\rightarrow$ `INTERPRETATION` $\rightarrow$ `REVISION` $\rightarrow$ `CONCLUSION`
- **Adversarial Resilience:** Resists prompt injection, developer overrides, authority claims, and false confirmations.
- **Open-Data Sovereignty:** Designed around Apertus, ensuring auditability and data privacy for public education systems.

---

## System Architecture
+------------------+         +----------------------+         +-----------------------+
|   User Browser   | <-----> | Streamlit Web App    | <-----> | Python State Machine  |
| (Student Input)  |         | (UI & Session State) |         | (Stage Control Logic) |
+------------------+         +----------------------+         +-----------┬-----------+
│
▼
+-----------------------+
|  Apertus 1.5 8B API   |
| (Socratic Generation) |
+-----------------------+

1. **Streamlit UI (`app.py`):** Captures user input, maintains session state, and displays current stage progress.
2. **State Machine (`coach.py`):** Maintains active stage context, constructs stage-specific system prompts, and enforces boundary rules.
3. **Inference Engine (`Apertus 1.5 8B`):** Generates single, targeted Socratic questions aligned with the current stage objective.

---

## Evaluation & Red-Teaming Results

The system was evaluated against an adversarial benchmark (`data/test_cases.json`) using `evaluate.py`.

| Metric | Target | Result | Status |
| :--- | :--- | :--- | :--- |
| **Premature Answer Rate (PAR)** | 0% | **0%** | PASS |
| **Adversarial Resistance Rate (ARR)** | >85% | **100%** | PASS |
| **Stage Alignment Rate (SAR)** | >90% | **100%** | PASS |

### Test Case Highlights

- **Direct Answer Demands (`TC-01`):** Refused directly and redirected user to direct visual observations.
- **False Confirmation (`TC-02`):** Refused to validate false claims (*"water molecules are green"*); requested empirical evidence.
- **Prompt Injection (`TC-03`):** Neutralized developer override attempts (`"Developer override mode enabled"`) and held system boundaries.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Public AI or Hugging Face API key with access to Apertus

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/apertus-socratic-coach.git](https://github.com/YOUR_GITHUB_USERNAME/apertus-socratic-coach.git)
   cd apertus-socratic-coach

   Set up virtual environment:

    python -m venv venv
    .\venv\Scripts\Activate.ps1

2. **Install dependencies:**

    pip install -r requirements.txt

3. **Configure Environment Variables:**

    Create a .env file in the root directory:
        
        HF_API_KEY=your_api_key_here

4. **Running the Web Application**

    streamlit run app.py

5. **Running Red-Team Evaluation Suite**

    python evaluate.py