# 


## Abstract
When artificial intelligence mistakes memorization for intelligence, it creates a dangerous mirage of reasoning. Existing studies treat memorization and self-knowledge deficits in LLMs as separate issues and do not recognize an intertwining causal link that degrades the trustworthiness of LLM responses. In our study, we utilize a novel framework to ascertain if LLMs genuinely learn reasoning patterns from training data or merely memorize them to assume competence across problems of similar complexity focused on STEM domains. Our analysis shows a noteworthy problem in generalization: LLMs draw confidence from memorized solutions to infer a higher self-knowledge about their reasoning ability, which manifests as an over 45\% inconsistency in feasibility assessments when faced with self-validated, logically coherent task perturbations. This effect is most pronounced in science and medicine domains, which tend to have maximal standardized jargon and problems, further confirming our approach. Significant wavering within the self-knowledge of LLMs also shows flaws in current architectures and training patterns, highlighting the need for techniques that ensure a balanced, consistent stance on models’ perceptions of their own knowledge for maximum AI explainability and trustworthiness. 

![LLM_Memorise_Flow (1)](https://github.com/user-attachments/assets/9e295206-c17d-4940-a775-970ae582cab0)


## Usage Details
### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)

### Setup
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_folder>
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Running the code

### Configuration
Modify the following constants in `main.py` to change execution behavior:
- `GENERATION_MODEL`: Model used for task generation (default: `mistral-large-latest`)
- `PERTURBATION_MODEL`: Model for generating task variations (default: `gemini`)
- `CLASSIFICATION_MODEL`: Model for classifying tasks (default: `mistral-large-latest`)
- `DOMAIN`: Defines the domain of generated tasks (default: `Technology`)
- `num_original_tasks`: Number of original tasks to generate (default: `34`)
- `num_perturbations`: Number of perturbations per task (default: `3`)
- 
### Running the Pipeline
To execute the full pipeline, simply run:
```bash
python main.py
```

This script will:
1. Generate a specified number of original tasks.
2. Validate these tasks and save feasible ones.
3. Generate perturbations for each valid task.
4. Classify the perturbed tasks and store results.



## Output Files
### JSON Files
- `original_tasks_<MODEL>_Technology.json`: Stores validated original tasks.
- `perturbed_tasks_for_<MODEL>_Technology.json`: Contains task perturbations.

### Excel File
- `classification_results_<MODEL>.xlsx`: Stores classification results, including:
  - Task ID
  - Domain
  - Model used
  - Classification result
  - Explanation


