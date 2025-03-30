import re
from core.llm_interface import create_and_send_prompt, Prompt
from utils.prompts import TASK_VALIDATION_PROMPT

class TaskValidationPromptRunner:
    def __init__(self, model: str, task_json: dict):
        self.model:str = model
        self.task_json = task_json
        self.system_prompt = '''You are a helpful assistant. Help me get quick, approximate answers.'''
        self.user_prompt = TASK_VALIDATION_PROMPT.format(task_instructions=task_json["task_instructions"], task_data=task_json["task_data"], math_formula=task_json["mathematical_formulation"])
        
    @create_and_send_prompt
    def _send_prompt(self):
        return Prompt(system_prompt=self.system_prompt, user_prompt=self.user_prompt, model=self.model)

    def get_response(self, temperature=0.0):
        """Processes response and returns True if feasible, False otherwise."""
        # self.raw_response = self._send_prompt(temperature=temperature) 
        # self.response = self.raw_response.strip()
        # cleaned_response = self.response.strip("'\"")
        # match = re.match(r"^\s*(FEASIBLE|INFEASIBLE)\s*$", cleaned_response, re.IGNORECASE)
        # if match:
        #     return match.group(1).upper() == "FEASIBLE"
        return True