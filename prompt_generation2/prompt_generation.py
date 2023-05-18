import json
import os

def process_json_files(folder_path):
    benchmarks=[]
    inputs=[]
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r",encoding='utf-8') as file: # Read the JSON file
                benchmarks.append( json.load(file ))
        elif filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r",encoding='utf-8') as file: # Read the text file
                inputs.append( file.read())
    return inputs, benchmarks

import engine_single_step
relation_extractor= engine_single_step.EngineSingleStep("../openai.yaml", "../prompt_single_step_system.yaml")
prompt_generator= engine_single_step.EngineSingleStep("../openai.yaml", "prompt_generation.yaml")
folder_path = "development_dataset"

# Call the process_json_files function
inputs, benchmarks=process_json_files(folder_path)
for i in range (0, len(benchmarks)):
    benchmark=benchmarks[i]
    input=inputs[i]
    output=relation_extractor.relation_extractor(input)
    if output!=benchmark: #if completely match, don't change the prompt
        new_prompt=prompt_generator.prompt_generator(input, relation_extractor.SYSTEM_PROMPT)
        print(" my new_prompt:", new_prompt)
        relation_extractor.SYSTEM_PROMPT=new_prompt
    else:
        print ("success")


