import os
import json
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
    output_file = os.path.join(output_dir, f"{title}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response)

    print(f"Response saved to {output_file}")


def load_credentials(credentials_file):
    with open(credentials_file, "r") as f:
        credentials = json.load(f)
    return credentials


def process_prompts_from_json(prompts_file, credentials_file="credentials.json",
                              role="I want you to act like a Senior Software Developer"
                              , model="TheBloke/CodeLlama-7B-Instruct-GGUF/codellama-7b-instruct.Q4_K_S.gguf"):
    with open(prompts_file, "r") as f:
        prompts_data = json.load(f)

    for prompt_data in prompts_data:
        prompt = prompt_data["prompt"]
        title = prompt_data["title"]
        query_llm_and_save(prompt, title, credentials_file=credentials_file, role=role, model=model)


if __name__ == "__main__":
    the_model = "TheBloke/CodeLlama-7B-Instruct-GGUF/codellama-7b-instruct.Q4_K_S.gguf"
    process_prompts_from_json("prompts.json", role="You are a Senior Software Developer specializing in Python,"
                                                   " each of the prompts are a part of a bigger mission so keep in"
                                                   " mind to write clean code that is easily integrated",
                              model=the_model)
