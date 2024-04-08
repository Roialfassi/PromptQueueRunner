## PromptQueueRunner
This Python script allows you to query a locally hosted Large Language Model (LLM) with multiple prompts and save the responses to text files. It provides a command-line interface for easy usage and configuration.

### Prerequisites
* Python 3.8+
* openai library (install with pip install openai)

### Usage
* Clone or download the repository to your local machine.
* Change the credentials to the api you are willing to use

if you are using LM studio then it is:
```json
{
    "base_url": "http://localhost:1234/v1",
    "api_key": "lm-studio"
}
```
Replace the values for "base_url" and "api_key" with the appropriate values
Create a JSON file (e.g., prompts.json) containing an array of prompt and title dictionaries. Example:
```json
[
    {
        "prompt": "Introduce yourself.",
        "title": "llm_introduction"
    },
    {
        "prompt": "What is the meaning of life?",
        "title": "meaning_of_life"
    },
    {
        "prompt": "Describe your favorite food.",
        "title": "favorite_food"
    }
]
```
Open a terminal or command prompt and navigate to the project directory.
Run the script with the following command:
```bash
python PromptQueueRunner.py -p prompts.json
```
This will process the prompts from the prompts.json file, query the local LLM with each prompt, and save the responses in the output/general folder with the corresponding titles as filenames.

## Command-line Arguments
The script supports the following command-line arguments:
* -p or --prompts: Path to the JSON file containing prompts and titles (required).
* -c or --credentials: Path to the JSON file containing LLM credentials (default: credentials.json).
* -o or --output: Path to the output folder where the response files will be saved (default: output).
* -t or --topic: Topic subfolder within the output folder where the response files will be saved (default: general).
* -s or --system: System role (instructions for the LLM) (default: "Always answer in rhymes.").

You can use the --help argument to display the help message and the available options:
```bash
python PromptQueueRunner.py --help
```
## Example
To run the script with custom options, use the following format:

```bash
python PromptQueueRunner.py -p prompts.json -c my_credentials.json -o my_output --topic science -s "Please respond in a scientific tone."
```
This will process the prompts from the prompts.json file, load the LLM credentials from the my_credentials.json file, save the responses in the my_output/science folder, and use the system role "Please respond in a scientific tone." when querying the LLM.

## Notes
* The script sanitizes the titles to ensure they are valid filenames. Characters that are not alphanumeric, underscore, hyphen, period, or parentheses are removed, and spaces are replaced with underscores.
* The responses from the LLM are saved as plain text files with the sanitized title as the filename.
* Make sure to update the credentials.json file with the correct credentials for your local LLM server.
* You can modify the prompts.json file to include different prompts and titles as needed.

## Creating prompts.json 
Go to GPT or Claude and enter the following prompt:
```text
Can you write me a json array with 30 prompts for 
{Your Subject}
each of the elements should have "title" and "prompt" 
title explains the objective of the prompt in 1 line
and prompt is the prompt itself
```
Then copy the prompts to the json and run it.

