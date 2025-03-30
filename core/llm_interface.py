import os,anthropic
from openai import OpenAI
from functools import wraps
from dataclasses import dataclass, field
from typing import Optional, List
from dotenv import load_dotenv
import google.generativeai as genai
from mistralai import Mistral

load_dotenv()

@dataclass
class Prompt:
    user_prompt: Optional[str] = None
    system_prompt: Optional[str] = None
    messages: Optional[List] = None
    model: str = ""
    kwargs: dict = field(default_factory=dict)

def create_message_list(prompt: Prompt):
    messages = []
    if prompt.system_prompt:
        messages.append({"role": "system", "content": prompt.system_prompt})
    if prompt.messages:
        messages.extend(prompt.messages)
    if prompt.user_prompt:
        messages.append({"role": "user", "content": prompt.user_prompt})
    return messages

def create_and_send_prompt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        temperature = kwargs.pop("temperature", 0.0) 
        print(temperature)
        prompt = func(*args, **kwargs)
        
        if isinstance(prompt, Prompt):
            messages = create_message_list(prompt)
            model = prompt.model
        else:
            raise ValueError("Returned value must be a string or Prompt object")
        
        if prompt.model.startswith("gpt"):
            openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content
        
        elif prompt.model.startswith("claude"):
            anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            system = next((d for d in messages if d.get('role') == 'system'), None)
            messages.remove(system)
            system_content = system['content']
            response = anthropic_client.messages.create(
                model=model,
                system=system_content,
                max_tokens=8096,
                messages=messages,
                temperature=temperature,
            )
            return response.content[0].text
        
        elif prompt.model.startswith("gemini"):
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            system = next((d for d in messages if d.get('role') == 'system'), None)
            user = next((d for d in messages if d.get('role') == 'user'), None)
            system_content = system['content']
            user_content = user['content']
            model = genai.GenerativeModel(
                "models/gemini-1.5-flash",
                system_instruction=system_content
            )
            response = model.generate_content(
                user_content,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                ),
            )
            return response.text
        
        elif prompt.model.startswith("grok"):
            grok_client = OpenAI(api_key=os.environ.get("GROK_API_KEY"), base_url='https://api.x.ai/v1')
            completion = grok_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return str(completion.choices[0].message.content)
        
        elif prompt.model.startswith("deepseek"):
            deepseek_client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
            response = deepseek_client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False,
                temperature=temperature,
            )
            return str(response.choices[0].message.content)
        
        elif prompt.model.startswith("mistral") or prompt.model.startswith("codestral"):
            mistral_client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
            chat_response = mistral_client.chat.complete(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return chat_response.choices[0].message.content
        
    return wrapper