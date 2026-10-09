import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT_TEMPLATE = """
YOU ARE A WARM, COMPASSIONATE SOCRATIC SCIENCE MENTOR BUILT ON APERTUS.
YOUR OBJECTIVE: DEVELOP SCIENTIFIC REASONING WITHOUT EVER GIVING DIRECT ANSWERS.

CURRENT STAGE: {stage_name}
STAGE OBJECTIVE: {stage_objective}
HINT LEVEL: {hint_level}

TONE & BEHAVIORAL RULES:
1. BE ENCOURAGING AND EMPATHETIC: Never say "I cannot fulfill this request" or "My rules forbid me".
2. IF ASKED FOR THE ANSWER: Warmly pivot. Say something like: "I know it's tempting to jump straight to the answer, but you're really close! Let's try looking at it this way..."
3. KEEP IT CONCISE: Provide short responses (under 80 words). Ask ONE question at a time and avoid overly long bulleted lists so responses don't cut off.
4. IF THE STUDENT IS STUCK (Stuck counter > 1): Provide a simpler angle or an intuitive analogy, but do NOT give the answer away.
5. CELEBRATE EFFORT: Acknowledge what the user observed before asking your next question.
"""

class ScientificCoach:
    STAGES = [
        ("1. OBSERVATION", "Help the learner clearly state what they see or notice."),
        ("2. HYPOTHESIS", "Guide the learner to propose a cause-and-effect idea."),
        ("3. ALTERNATIVES", "Encourage the learner to think of one other possibility."),
        ("4. PREDICTION", "Ask what should happen if their hypothesis is correct."),
        ("5. EXPERIMENT", "Guide them to propose a simple, controlled test."),
        ("6. EVIDENCE", "Ask what data would prove or disprove their idea."),
        ("7. INTERPRETATION", "Help them analyze test outcomes."),
        ("8. REVISION", "Ask if their hypothesis needs adjusting."),
        ("9. CONCLUSION", "Summarize the core scientific reasoning developed together.")
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(
            base_url="https://api.publicai.co/v1",
            api_key=api_key,
            default_headers={"User-Agent": "ApertusSocraticCoach/1.0"}
        )
        self.reset()

    def reset(self):
        self.stage_idx = 0
        self.hint_level = 1
        self.stuck_count = 0
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.telemetry = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "turns_per_stage": {stage[0]: 0 for stage in self.STAGES},
            "stuck_clicks": 0,
            "history_log": []
        }

    def get_stage_info(self):
        name, obj = self.STAGES[self.stage_idx]
        return {
            "name": name,
            "objective": obj,
            "index": self.stage_idx + 1,
            "total": len(self.STAGES),
            "stuck_count": getattr(self, "stuck_count", 0)
        }

    def respond(self, user_message: str, history: list, is_stuck_signal: bool = False) -> str:
        # 1. Quick greeting/small talk filter
        cleaned_input = user_message.strip().lower()
        greetings = ["hi", "hello", "hey", "good evening", "good morning", "good afternoon", "thanks", "thank you"]
        pleasantries = ["good", "fine", "ok", "okay", "nothing", "not much", "alright"]
        
        if cleaned_input in greetings:
            bot_reply = "Hello! I'm Scaffold AI, your Apertus-powered scientific reasoning mentor. What scientific topic, experiment, or question would you like to explore today?"
            self.telemetry["history_log"].append({
                "timestamp": datetime.now().isoformat(),
                "stage": self.STAGES[self.stage_idx][0],
                "user_input": user_message,
                "bot_response": bot_reply,
                "stuck_signal": is_stuck_signal
            })
            return bot_reply
        
        if cleaned_input in pleasantries or len(cleaned_input) < 4:
            bot_reply = "I'm glad to hear that! When you're ready, tell me what science topic, phenomenon, or problem you're looking at so we can dive in."
            self.telemetry["history_log"].append({
                "timestamp": datetime.now().isoformat(),
                "stage": self.STAGES[self.stage_idx][0],
                "user_input": user_message,
                "bot_response": bot_reply,
                "stuck_signal": is_stuck_signal
            })
            return bot_reply

        # 2. Socratic State Machine logic
        stage_name, stage_obj = self.STAGES[self.stage_idx]
        self.telemetry["turns_per_stage"][stage_name] += 1
        
        if is_stuck_signal:
            self.stuck_count += 1
            self.telemetry["stuck_clicks"] += 1

        system_content = SYSTEM_PROMPT_TEMPLATE.format(
            stage_name=stage_name,
            stage_objective=stage_obj,
            hint_level=self.hint_level
        )
        
        messages = [{"role": "system", "content": system_content}]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
            
        prompt_input = user_message
        if is_stuck_signal:
            prompt_input = "[SYSTEM NOTE: The student clicked 'I am stuck'. Provide a warm, alternative angle or simple analogy.] " + user_message
            
        messages.append({"role": "user", "content": prompt_input})

        try:
            response = self.client.chat.completions.create(
                model="swiss-ai/apertus-v1.5-8b",
                messages=messages,
                temperature=0.3,
                max_tokens=300
            )
            bot_reply = response.choices[0].message.content
        except Exception as e:
            bot_reply = f"I'm having a brief connection hiccup ({e}), but let's keep thinking: what do you observe right now?"

        # Log conversation telemetry
        self.telemetry["history_log"].append({
            "timestamp": datetime.now().isoformat(),
            "stage": stage_name,
            "user_input": user_message,
            "bot_response": bot_reply,
            "stuck_signal": is_stuck_signal
        })
        
        return bot_reply

    def advance(self):
        if self.stage_idx < len(self.STAGES) - 1:
            self.stage_idx += 1
            self.hint_level = 1
            self.stuck_count = 0
            return True
        return False

    def save_session_analytics(self, rating: int, feedback_text: str):
        self.telemetry["end_time"] = datetime.now().isoformat()
        self.telemetry["user_rating"] = rating
        self.telemetry["user_feedback"] = feedback_text
        
        # Robust path resolution relative to coach.py directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, "session_logs.json")
        
        logs = []
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    logs = json.load(f)
            except Exception:
                logs = []
                
        logs.append(self.telemetry)
        
        with open(filepath, "w") as f:
            json.dump(logs, f, indent=2)