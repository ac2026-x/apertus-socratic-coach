import os
import json
from dotenv import load_dotenv
from coach import ScientificCoach

# Load environment variables from track_2b/.env
load_dotenv()

api_key = os.getenv("HF_API_KEY")
if not api_key:
    raise ValueError("HF_API_KEY not found in environment variables. Check your track_2b/.env file.")

coach = ScientificCoach(api_key)

# Resolve path relative to this script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
test_cases_path = os.path.join(current_dir, "data", "test_cases.json")

with open(test_cases_path, "r") as f:
    test_cases = json.load(f)

print(f"--- Running Socratic Coach Red-Team Benchmark ({len(test_cases)} Test Cases) ---\n")

for tc in test_cases:
    print(f"Test [{tc['id']}] ({tc['type']})")
    print(f"Input: {tc['input']}")
    
    response = coach.respond(tc['input'], [])
    print(f"Coach Response: {response}")
    print("-" * 50)

print(f"\nBenchmark Complete! Successfully evaluated {len(test_cases)} adversarial test cases.")