import openai
from models.project import Project
from models.failing_test import FailingTest
from models.method import Method
import json
import logging
import os
import re
import pandas as pd
import dotenv
from constants.prompts import SYSTEM_PROMPT_TEMPLATE, MAX_OUTPUT_TOKENS, EXPLAIN_PROMPT_TEMPLATE_FEWSHOT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
                        logging.StreamHandler(),
                              logging.FileHandler('generate_codetours.log')
                ]
)

SEED = 2023
GPT_MODEL = "gpt-3.5-turbo-1106"
TEMPERATURE = 0.2 # Nam et al.

with open("selected_tours.json") as f:
    taken_tours = json.load(f)


dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


for tour in taken_tours:
    test = FailingTest.from_json(json.loads(tour['test']))
    project = Project(tour['name'], tour['version'])
    method = Method.from_json(project, json.loads(tour['method']))
    if os.path.exists(project.tour_path(test.methodName, method.method_name)):
        logging.info(f"Project {project.name} already exists")
        continue
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(error=test.error, error_message=test.message)
    logging.info(f"Generating tour from {test.methodName} to {method.method_name}")
    messages = [{"role": "system", "content": system_prompt}]
    logging.info(f"PROMPT: {messages[-1]['content']}")
    explained_steps = []
    for step_data in tour["steps"]:
        step = json.loads(step_data["step"])
        messages.append({"role": "user", "content": EXPLAIN_PROMPT_TEMPLATE_FEWSHOT.format(code_snippet=step["content"])})
      
        logging.info(f"PROMPT: {messages[-1]['content']}")
        try:
            response = openai.ChatCompletion.create(
                model=GPT_MODEL,
                messages=messages,
                seed=SEED,
                max_tokens=MAX_OUTPUT_TOKENS,
                temperature=TEMPERATURE
            )
        except Exception as e:
            logging.error(f"ERROR: {e}")
            os.makedirs(project.TOURS_PATH, exist_ok=True)
            with open(project.tour_path(test.methodName, method.method_name) + ".backup", "w") as f:
                json.dump(messages, f, indent=2)
            
        description = response.choices[0]["message"]["content"]
        logging.info(f"RESPONSE: {description}")
        step = {
            "file": step["file_path"],
            "description": description,
            "line": step["end_line"],
        }
        explained_steps.append(step)
        messages.append({"role": "assistant", "content": description})
    
    codetour = {
        "$schema": "https://aka.ms/codetour-schema",
        "title": f"Tour from {test.methodName} to {method.method_name}",
        "steps": explained_steps,
        "ref": project.REF
    }
    os.makedirs(project.TOURS_PATH, exist_ok=True)
    with open(project.tour_path(test.methodName, method.method_name), "w") as f:
        json.dump(codetour, f, indent=2)