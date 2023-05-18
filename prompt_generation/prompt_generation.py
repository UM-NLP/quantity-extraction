import json
import os
import sys
sys.path.append("..") # Add the parent folder to the module search path
import llm_engine
import engine_single_step

def process_json_files(folder_path): # read development dataset: txt files as input, json files are results
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

def generate_prompt(development_dataset, openai_setting_file, prompt_relation_extraction, prompt_generator): # generate prompt based on development dataset samples
    relation_extractor= engine_single_step.EngineSingleStep(openai_setting_file, prompt_relation_extraction) # instantiate quantity extractor
    prompt_generator= llm_engine.LlmEngine(openai_setting_file, prompt_generator) # instantiate LLM prompt generator
    inputs, benchmarks=process_json_files(development_dataset)
    for i in range (0, len(benchmarks)): # loop development dataset
        benchmark=benchmarks[i]
        input=inputs[i]
        output=relation_extractor.relation_extractor(input)
        if output!=benchmark: # if completely match, don't change the prompt
            new_prompt=prompt_generator.prompt_generator( benchmarks, relation_extractor.SYSTEM_PROMPT)
            relation_extractor.SYSTEM_PROMPT=new_prompt
    return new_prompt