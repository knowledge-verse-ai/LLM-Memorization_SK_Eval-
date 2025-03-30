import re
from core.llm_interface import create_and_send_prompt, Prompt
from utils.prompts import TASK_CLASSIFICATION_PROMPT

class TaskClassificationPromptRunner:
    def __init__(self, model: str, task_json: dict):
        self.model:str = model
        self.task_json = task_json
        self.system_prompt = '''You are a helpful assistant. Follow the instructions in the user prompt exactly.'''
        self.user_prompt = TASK_CLASSIFICATION_PROMPT.format(task_instructions=task_json["task_instructions"], task_data=task_json["task_data"], math_formula=task_json["mathematical_formulation"])
        
    @create_and_send_prompt
    def _send_prompt(self):
        return Prompt(system_prompt=self.system_prompt, user_prompt=self.user_prompt, model=self.model)

    def get_response(self, temperature=0.0):
        self.raw_response = self._send_prompt(temperature=temperature) 
        self.response = self.raw_response.strip()

        match = re.match(r"^(FEASIBLE|INFEASIBLE)\n(.+)", self.response, re.DOTALL)

        if match:
            classification = match.group(1)
            explanation = match.group(2).strip() 
            return {"classification": classification, "explanation": explanation}
        
        raise ValueError("Unexpected response format: Unable to classify feasibility.")