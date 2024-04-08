import os
import json
import argparse
import string
from openai import OpenAI


def load_credentials(credentials_file):
    with open(credentials_file, "r") as f:
        credentials = json.load(f)
    return credentials


def sanitize_filename(title):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in title if c in valid_chars)
    sanitized = sanitized.replace(' ', '_')
    return sanitized


def query_llm_and_save(prompt, title, output_folder, topic, system_role, credentials_file="credentials.json"):
    # Load credentials from JSON file
    credentials = load_credentials(credentials_file)

    # Example: reuse your existing OpenAI setup
    # Point to the local server
    client = OpenAI(base_url=credentials["base_url"], api_key=credentials["api_key"])

    completion = client.chat.completions.create(
        model="Loaded from Chat UI",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    response = completion.choices[0].message.content

    # Create the output directory and topic subfolder if they don't exist
    topic_folder = os.path.join(output_folder, topic)
    os.makedirs(topic_folder, exist_ok=True)

    # Sanitize the title to make it a valid filename
    sanitized_title = sanitize_filename(title)

    # Save the response to a .txt file in the topic subfolder
    output_file = os.path.join(topic_folder, f"{sanitized_title}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response)

    print(f"Response saved to {output_file}")


def process_prompts_from_json(prompts_file, output_folder, topic, system_role, credentials_file="credentials.json"):
    with open(prompts_file, "r") as f:
        prompts_data = json.load(f)

    for prompt_data in prompts_data:
        prompt = prompt_data["prompt"]
        title = prompt_data["title"]
        query_llm_and_save(prompt, title, output_folder, topic, system_role, credentials_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query a local LLM and save responses to text files.")
    parser.add_argument("-p", "--prompts", required=True, help="Path to the JSON file containing prompts and titles")
    parser.add_argument("-c", "--credentials", default="credentials.json",
                        help="Path to the JSON file containing LLM credentials (default: credentials.json)")
    parser.add_argument("-o", "--output", default="output", help="Path to the output folder (default: output)")
    parser.add_argument("-t", "--topic", default="general",
                        help="Topic subfolder within the output folder (default: general)")
    parser.add_argument("-s", "--system", default="I want you to act like a Senior Software Developer",
                        help="System role (instructions for the LLM)")

    args = parser.parse_args()

    process_prompts_from_json(args.prompts, args.output, args.topic, args.system, args.credentials)
