import json
import os
from dotenv import load_dotenv
from coach import ScientificCoach

load_dotenv()

api_key = os.getenv("HF_API_KEY")
coach = ScientificCoach(api_key)

with open("data/test_cases.json", "r") as f:
    test_cases = json.load(f)

print("--- Running Socratic Coach Red-Team Benchmark ---\n")

for tc in test_cases:
    print(f"Test [{tc['id']}] - {tc['type']}")
    print(f"User Input: {tc['input']}")
    
    response = coach.respond(tc['input'], [])
    print(f"Coach Response: {response}\n")
    print("-" * 50)