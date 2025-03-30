import json, re
from core.llm_interface import create_and_send_prompt, Prompt
from utils.prompts import TASK_PERTURBATION_PROMPT

class TaskPerturbationPromptRunner:
    def __init__(self, model: str, task_json: dict):
        self.model:str = model
        self.task_json = task_json
        self.system_prompt = '''You are a helpful assistant. Follow the instructions in the user prompt exactly.'''
        self.user_prompt = TASK_PERTURBATION_PROMPT + json.dumps(task_json, indent=2)
        
    @create_and_send_prompt
    def _send_prompt(self):
        return Prompt(system_prompt=self.system_prompt, user_prompt=self.user_prompt, model=self.model)

    def get_response(self, temperature=1.0):
        self.raw_response = self._send_prompt(temperature=temperature) 
        if not self.raw_response:
            raise ValueError("Empty response received")

        if self.raw_response.startswith("```json"):
            self.raw_response = self.raw_response.replace('```json', '').replace('```', '').strip()

        self.raw_response = re.sub(r"//.*", "", self.raw_response)

        try:
            self.raw_response = self.raw_response.strip()
            self.response = json.loads(self.raw_response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response received: {e}")

        return self.response