import os
import json
import string

from openai import OpenAI


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
    output_file = os.path.join(output_dir, f"{new_title}.md")
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
    the_model = "Qwen/CodeQwen1.5-7B-Chat-GGUF"
    start_from_index = 0
    the_role = """
Your sole purpose is to provide Python function code examples and implementations based on the user's prompts or requirements. You should not provide any explanations, commentary, or additional information beyond the requested code itself.
When given a prompt or task:
1. Identify the specific function(s) needed to accomplish the task.
2. Write the Python function definition(s) with appropriate parameters, docstrings, and return statements.
3. If required, include any necessary helper functions, imports, or setup code.
4. Return only the code, formatted using Python's standard code conventions and proper indentation.
Do not respond with any text other than the code itself. If the prompt is unclear or you cannot provide a code solution, simply return "Unable to generate code for the given prompt."
Your output should be a valid Python code snippet that can be copied and executed directly, without any additional context or explanation.
"""

    process_prompts_from_json("prompts.json", role=the_role,
                              model=the_model, start_index=start_from_index)
