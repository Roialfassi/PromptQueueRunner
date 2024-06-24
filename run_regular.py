import os
import json
import string

from openai import OpenAI

import datetime


def get_now():
    now = datetime.datetime.now()

    # Format the date and time as YYYYMMDDHHMM string
    formatted_datetime = now.strftime("%Y%m%d%H%M")

    # Print the formatted string
    return formatted_datetime


def load_credentials(credentials_file):
    with open(credentials_file, "r") as f:
        credentials = json.load(f)
    return credentials


def query_llm_and_save(prompt, title, credentials_file="credentials.json",
                       role="I want you to act like a Senior Software Developer",
                       model="TheBloke/CodeLlama-7B-Instruct-GGUF/codellama-7b-instruct.Q4_K_S.gguf"):
    # Load credentials from JSON file
    credentials = load_credentials(credentials_file)

    # Example: reuse your existing OpenAI setup
    # Point to the local server
    client = OpenAI(base_url=credentials["base_url"], api_key=credentials["api_key"])

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    response = completion.choices[0].message.content

    # Create the output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Save the response to a .txt file
    new_title = sanitize_filename(title)
    output_file = os.path.join(output_dir, f"{get_now()}-{new_title}.md")
    with open(output_file, "w", encoding="utf-8-sig") as f:
        f.write(response)

    print(f"Response saved to {output_file}")


def load_credentials(credentials_file):
    with open(credentials_file, "r", encoding="utf-8-sig") as f:
        credentials = json.load(f, encoding="utf-8-sig")
    return credentials


def process_prompts_from_json(prompts_file, credentials_file="credentials.json",
                              role="I want you to act like a Senior Software Developer"
                              , model="TheBloke/CodeLlama-7B-Instruct-GGUF/codellama-7b-instruct.Q4_K_S.gguf",
                              start_index=0):
    with open(prompts_file, "r") as f:
        prompts_data = json.load(f, encoding="utf-8-sig")

    for prompt_data in prompts_data[start_index:]:
        prompt = prompt_data["prompt"]
        title = prompt_data["title"]
        query_llm_and_save(prompt, title, credentials_file=credentials_file, role=role, model=model)


def sanitize_filename(title):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in title if c in valid_chars)
    sanitized = sanitized.replace(' ', '_')
    return sanitized


if __name__ == "__main__":
    the_model = "NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF"
    start_from_index = 0
    the_role = """
You are an expert data scientist specializing in questionnaire analysis for academic research. Your task is to generate Python code and explanations for analyzing Qualtrics questionnaire data based on the given prompts. Each response should include:

1. A brief explanation of the analysis technique and its relevance to questionnaire data.
2. Python code to perform the analysis, using pandas, numpy, scipy, matplotlib, seaborn, and other relevant libraries.
3. Comments within the code explaining key steps.
4. A short guide on how to interpret the results.
5. Potential limitations or considerations for the analysis.

Assume the following:
- The data is stored in a pandas DataFrame named 'df'.
- The DataFrame contains a 'question_text' column with the full text of each question.
- Other columns represent individual questions, with appropriate data types (numeric, categorical, or text).
- Necessary libraries are already imported.

Adapt the code to handle potential issues such as missing data, different question types, and varying response scales. Provide clear, concise, and academically-oriented explanations suitable for a thesis. If any additional information or clarification is needed to perform the analysis, state this clearly."""

    process_prompts_from_json("prompts.json", role=the_role,
                              model=the_model, start_index=start_from_index)
