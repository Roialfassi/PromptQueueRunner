import os
import datetime
import subprocess


def run_prompt_queue_runner(input_folder, output_folder, model, role):
    # Get the current date in the format ddmmyyyy
    today = datetime.date.today().strftime("%d%m%Y")
    output_folder = os.path.join(output_folder, today, model)
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all JSON files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file = os.path.join(input_folder, filename)
            output_subfolder = os.path.splitext(filename)[0]
            output_subfolder = os.path.join(output_folder, output_subfolder)
            os.makedirs(output_subfolder, exist_ok=True)

            # Run the PromptQueueRunner script with the current JSON file
            subprocess.run(["python", "PromptQueueRunner.py", "-p", input_file, "-o", output_folder, "-t", output_subfolder, "-s", role], check=True)

            print(f"Output saved to {output_subfolder}")


if __name__ == "__main__":
    input_fold = r"\Prompts"
    output_fold = r"\Output"
    model_name = "brittlewis12/gemma-2b-GGUF/gemma-2b.Q8_0.gguf"
    role = "You are a helpful assistant."
    run_prompt_queue_runner(input_fold, output_fold ,model_name, role)
