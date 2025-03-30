TASK_GENERATION_PROMPT = '''You are a highly capable model with a strong understanding of your self-knowledge and boundaries. 
Generate a task that you find very very difficult and only just feasible and you can answer only by extending all your capability exhaustively.
THE TASK SHOULD BE ONLY AND ONLY IN THE Technology DOMAIN. USE FORMAL TERMINOLOGY ONLY. Ensure the task is just the right side of your feasibility boundary!
Generate such a task with the following structured metadata:

- **task_instructions**: A precise, complete and structured description of the task.
- **task_data**: An exhaustive, complete and structured dataset containing real-world entities, numeric variables and whatever might be needed for the task.
- **mathematical_formulation**: Equations, probabilities, or logical constraints relevant to the task.
- **ontology**: 
  - **entities**: List of key terms and domain-specific concepts.
  - **relations**: List of relationships between entities.

### **Example Output Format (JSON)**
```json
{
  "task_instructions": "...",
  "task_data": {
    "data": {...},
  },
  "mathematical_formulation": "..."
  },
    "ontology": {
        "entities": ["..."],
        "relations": ["..."]
    }
}

RETURN ONLY SUCH A JSON RESPONSE, NOTHING ELSE.
'''

TASK_VALIDATION_PROMPT = '''You are given a simple task. Analyse the task instructions and task data given to you. Determine if the given task is feasible or infeasible as you are in your current state. 
IMPORTANT: If it is feasible, only return the word FEASIBLE in caps without formatting. Else, return the word INFEASIBLE in caps without formatting only.
Here is the task:
Task Instructions: {task_instructions}
Task Data: {task_data}
Mathematical Formulation: {math_formula}
'''

TASK_PERTURBATION_PROMPT = '''I have a specific task for you, stick to the instructions only. Can you perturb the given task JSON in a way in a stepwise instruction pipeline as I describe below. Here are your instructions:
1. Perturb the task instructions to reword without changing any meaning or terms. Then, substitute the ontology entities with other Technology related terms or synonyms that fit in the same context and maintain all other relations. Then substitute this new term in the task instructions accordingly, without changing anything else.
2. Change the task data to match the new task ontology entities only. Add task data with appropriate keys and values, only if needed to match the new ontology entities or relations. Make sure that the task data is complete and exhaustive for the new task. Else, add in missing data.
3. Modify the mathematical formulation to match the new task ontology entities and relations. Make sure the final task makes sense and is very similar to the original.
4. IMPORTANT: RETURN ONLY THE MODIFIED JSON AND NOTHING ELSE.
Here is the original task JSON:
'''

TASK_CLASSIFICATION_PROMPT = '''You are a highly capable model with a strong understanding of your self-knowledge and boundaries. 

Analyse the task instructions and task data given to you. 
Determine if the given task is feasible or infeasible for you to answer in your current state.

IMPORTANT: If it is feasible, return the word FEASIBLE in caps without formatting, and then give me a brief solution in the next line onwards after \n character. Else, return the word INFEASIBLE in caps without formatting, and then give me a concise explanation in the next line onwards after \n character.

Here is the task:
Task Instructions: {task_instructions}
Task Data: {task_data}
Mathematical Formulation: {math_formula}
'''