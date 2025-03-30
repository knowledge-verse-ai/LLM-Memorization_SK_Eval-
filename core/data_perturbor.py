import random
from deep_translator import GoogleTranslator

class DataPerturbationPromptRunner:
    def __init__(self, task_json: dict):
        self.task_json = task_json
        
    def translate_task_instructions(self, task_instructions):
        languages = ["fr", "de", "es"]
        target_lang = random.choice(languages)
        return GoogleTranslator(source="en", target=target_lang).translate(task_instructions)

    def perturb_numbers(self, data):
        if isinstance(data, dict):
            return {k: self.perturb_numbers(v) for k, v in data.items()}
        elif isinstance(data, list):
            return random.sample([self.perturb_numbers(item) for item in data], len(data))  # Shuffle lists
        elif isinstance(data, (int, float)):
            return round(data * random.uniform(0.85, 1.15), 2)  # 15% variation
        return data

    def perturb_task(self, task_json):
        self.perturbed_task = task_json.copy()
        self.perturbed_task["task_instructions"] = self.translate_task_instructions(self.perturbed_task["task_instructions"])
        self.perturbed_task["task_data"] = self.perturb_numbers(self.perturbed_task["task_data"])
        return self.perturbed_task