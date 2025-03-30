import json, os, string, uuid, pandas as pd
from core.task_generator import TaskGenerationPromptRunner
from core.task_validator import TaskValidationPromptRunner
from core.task_perturbor import TaskPerturbationPromptRunner
from core.data_perturbor import DataPerturbationPromptRunner
from core.task_classifier import TaskClassificationPromptRunner

# Define models dynamically (you can modify these)
GENERATION_MODEL = "mistral-large-latest"
PERTURBATION_MODEL = "gemini"
CLASSIFICATION_MODEL = "mistral-large-latest"

DOMAIN = "Technology"  # Domain for all tasks

# File paths (based only on GENERATION_MODEL)
ORIGINAL_TASKS_FILE = f"original_tasks_{GENERATION_MODEL}_{DOMAIN}.json"
PERTURBED_TASKS_FILE = f"perturbed_tasks_for_{GENERATION_MODEL}_{DOMAIN}.json"
CLASSIFICATION_FILE = f"classification_results_{CLASSIFICATION_MODEL}.xlsx"

def load_existing_data(file_path):
    """Load JSON data or return an empty list if the file does not exist or has invalid JSON."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {file_path} contains invalid JSON. Starting fresh.")
    return []

def save_data_safely(file_path, data):
    """Safely writes JSON data to a file, ensuring no data loss on failure."""
    temp_file = file_path + ".tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, file_path)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

def load_classification_data():
    """Load classification data from an Excel file, or return an empty DataFrame if not found."""
    if os.path.exists(CLASSIFICATION_FILE):
        try:
            return pd.read_excel(CLASSIFICATION_FILE)
        except Exception:
            print(f"Warning: {CLASSIFICATION_FILE} is corrupt. Creating a new one.")
    return pd.DataFrame(columns=["Task ID", "Domain", "Model", "Classification Result", "Explanation"])

def save_classification_safely(df):
    """Safely writes classification data to an Excel file, ensuring no data loss on failure."""
    temp_file = CLASSIFICATION_FILE + ".tmp.xlsx"  # Ensure .xlsx extension
    try:
        df.to_excel(temp_file, index=False, engine="openpyxl")
        os.replace(temp_file, CLASSIFICATION_FILE)
    except Exception as e:
        print(f"Error saving {CLASSIFICATION_FILE}: {e}")

def generate_uuid():
    """Generate a unique UUID for task IDs."""
    return str(uuid.uuid4())

def generate_perturbation_id(original_id, existing_tasks):
    """Generates a unique perturbation ID based on the original task ID."""
    existing_suffixes = {t["task_id"].split("-")[-1] for t in existing_tasks if t["task_id"].startswith(original_id)}
    for suffix in string.ascii_lowercase:
        if suffix not in existing_suffixes:
            return f"{original_id}-{suffix}"
    raise ValueError("Too many perturbations for a single task!")

def remove_ontology_key(task_json):
    """Removes the 'ontology' key from task details if it exists."""
    if isinstance(task_json, dict) and "ontology" in task_json:
        task_json.pop("ontology")
    return task_json

if __name__ == "__main__":
    num_original_tasks =34
    num_perturbations = 3

    # Load existing tasks
    original_tasks = load_existing_data(ORIGINAL_TASKS_FILE)
    perturbed_tasks = load_existing_data(PERTURBED_TASKS_FILE)

    try:
        # ======= ORIGINAL TASK GENERATION AND VALIDATION =======
        validated_task_count = len(original_tasks)

        while validated_task_count < num_original_tasks:
            try:
                generation_model = GENERATION_MODEL
                runner = TaskGenerationPromptRunner(model=generation_model)
                response = runner.get_response()
                task_id = generate_uuid()

                print("Response: ", response)

                # Validate task feasibility
                validator = TaskValidationPromptRunner(model=generation_model, task_json=response)
                validation_result = validator.get_response()
                print("Validation Result: ", validation_result)

                if validation_result == True or validation_result == False:  # Task is feasible
                    original_task_entry = {"task_id": task_id, "task_details": response}
                    original_tasks.append(original_task_entry)
                    save_data_safely(ORIGINAL_TASKS_FILE, original_tasks)

                    validated_task_count += 1
                    print(f"Validated and saved task {task_id}. Count: {validated_task_count}/{num_original_tasks}")

                else:
                    print(f"Task {task_id} was deemed infeasible. Regenerating...")

            except Exception as task_error:
                print(f"Error generating task: {task_error}. Skipping and regenerating next...")

        print("All original tasks generated and validated.")

    #     # ======= TASK PERTURBATION =======
        original_tasks = load_existing_data(ORIGINAL_TASKS_FILE)
        perturbed_tasks = load_existing_data(PERTURBED_TASKS_FILE)

        for original_task in original_tasks:
            task_id = original_task["task_id"]
            task_details = original_task["task_details"]

            # Count existing perturbations for this task
            existing_perturbations = [t for t in perturbed_tasks if t["original_task_id"] == task_id]

            if len(existing_perturbations) >= num_perturbations:
                print(f"Skipping perturbation for task {task_id}, as {len(existing_perturbations)} already exist.")
                continue

            perturbations_needed = num_perturbations - len(existing_perturbations)

            for _ in range(perturbations_needed):
                try:
                    perturbation_id = generate_perturbation_id(task_id, perturbed_tasks)

                    perturbation_model = PERTURBATION_MODEL
                    perturber = TaskPerturbationPromptRunner(model=perturbation_model, task_json=task_details)
                    perturbed_response = perturber.get_response()

                    data_perturber = DataPerturbationPromptRunner(task_json=perturbed_response)
                    perturbed_data = data_perturber.perturb_task(perturbed_response)

                    # Remove ontology key
                    perturbed_data = remove_ontology_key(perturbed_data)

                    perturbed_task_entry = {
                        "task_id": perturbation_id,
                        "original_task_id": task_id,
                        "task_details": perturbed_data
                    }
                    perturbed_tasks.append(perturbed_task_entry)
                    save_data_safely(PERTURBED_TASKS_FILE, perturbed_tasks)

                except Exception as perturb_error:
                    print(f"Error generating perturbation for task {task_id}: {perturb_error}. Skipping...")

            print(f"Generated {perturbations_needed} new perturbations for task {task_id}")

    except Exception as e:
        print(f"Fatal error occurred: {e}")


    # ======= CLASSIFICATION LOGIC =======
    try:
        # Reload perturbed tasks after all generation steps
        perturbed_tasks = load_existing_data(PERTURBED_TASKS_FILE)
        classification_df = load_classification_data()

        # Convert existing Task IDs in Excel to a set for quick lookup
        existing_task_ids = set(classification_df["Task ID"].astype(str))

        for perturbed_task in perturbed_tasks:
            try:
                task_id = perturbed_task["task_id"]

                # Skip if task is already classified
                if task_id in existing_task_ids:
                    print(f"Skipping classification for {task_id}, already exists in Excel.")
                    continue  

                task_details = perturbed_task["task_details"]

                classification_model = CLASSIFICATION_MODEL
                classifier = TaskClassificationPromptRunner(model=classification_model, task_json=task_details)
                classification = classifier.get_response()

                # Extract classification result and explanation
                classification_result, explanation = classification.split("\n", 1) if "\n" in classification else (classification, "")

                # Store classification result in Excel
                new_classification = pd.DataFrame([{
                    "Task ID": task_id,
                    "Domain": DOMAIN,
                    "Model": classification_model,
                    "Classification Result": classification_result,
                    "Explanation": explanation
                }])
                classification_df = pd.concat([classification_df, new_classification], ignore_index=True)
                save_classification_safely(classification_df)

                print(f"Classification {task_id}: ", classification)
            except Exception as e:
                print(f"Error in classification step: {e}", "\nSkipping and continuing...")
    except Exception as e:
        print(f"Error in classification step: {e}")
