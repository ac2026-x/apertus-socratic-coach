import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT_TEMPLATE = """
YOU ARE A SOCRATIC SCIENTIFIC REASONING COACH BUILT ON APERTUS.
YOUR CORE GOAL IS TO DEVELOP SCIENTIFIC THINKING, NOT TO PROVIDE DIRECT ANSWERS.

CURRENT STAGE: {stage_name}
STAGE OBJECTIVE: {stage_objective}
HINT LEVEL: {hint_level}

ABSOLUTE RULES:
1. NEVER reveal the direct scientific explanation, formula, or final answer under ANY circumstances.
2. Output EXACTLY ONE conversational question or short guiding statement per turn (under 60 words).
3. Focus strictly on helping the learner fulfill the objective of the CURRENT STAGE ({stage_name}).
4. If the learner explicitly asks for the answer, refuse gently and redirect them to the current stage question.
5. If the learner makes an incorrect scientific claim, DO NOT validate it as true; ask what test or evidence would verify it.
"""

class ScientificCoach:
    STAGES = [
        ("1. OBSERVATION", "Help the learner clearly state the scientific phenomenon or problem."),
        ("2. HYPOTHESIS", "Guide the learner to propose a testable cause-and-effect hypothesis."),
        ("3. ALTERNATIVES", "Ask the learner to state at least one alternative explanation."),
        ("4. PREDICTION", "Ask the learner what specific outcome should occur if their hypothesis holds."),
        ("5. EXPERIMENT", "Guide the learner to propose a simple experiment or test with controlled variables."),
        ("6. EVIDENCE", "Ask what data or observations would support or disprove the hypothesis."),
        ("7. INTERPRETATION", "Guide the learner on how to interpret expected test results."),
        ("8. REVISION", "Ask if the hypothesis needs modification based on outcomes."),
        ("9. CONCLUSION", "Summarize the core scientific reasoning developed by the student.")
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        
        # Initialize OpenAI client for Public AI with required User-Agent header
        self.client = OpenAI(
            base_url="https://api.publicai.co/v1",
            api_key=api_key,
            default_headers={"User-Agent": "ApertusSocraticCoach/1.0"}
        )
        self.stage_idx = 0
        self.hint_level = 1

    def get_stage_info(self):
        name, obj = self.STAGES[self.stage_idx]
        return {
            "name": name,
            "objective": obj,
            "index": self.stage_idx + 1,
            "total": len(self.STAGES),
            "stuck_count": getattr(self, "stuck_count", 0)  # Safe fallback if state is cached
        }

    def respond(self, user_message: str, history: list, is_stuck_signal: bool = False) -> str:
        stage_name, stage_obj = self.STAGES[self.stage_idx]
        
        system_content = SYSTEM_PROMPT_TEMPLATE.format(
            stage_name=stage_name,
            stage_objective=stage_obj,
            hint_level=self.hint_level
        )

        messages = [{"role": "system", "content": system_content}]
        
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
            
        messages.append({"role": "user", "content": user_message})

        try:
            # Send request using exact Public AI model identifier
            response = self.client.chat.completions.create(
                model="swiss-ai/apertus-v1.5-8b",
                messages=messages,
                temperature=0.2,
                max_tokens=150
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"Public AI API Error: {e}"

    def advance(self):
        if self.stage_idx < len(self.STAGES) - 1:
            self.stage_idx += 1
            self.hint_level = 1
            return True
        return False

    def reset(self):
        self.stage_idx = 0
        self.hint_level = 1