
# Quantity Measurement Extraction
## Project Description
This project provide methods to extract measurements and their values from unstructured text. <br />
It extracts four types of entities and their relations: <br />
1. entity: Any quantitative physical object or any measurable component or substance. <br />
2. property: It can be any physical, biological, or chemical characteristics of any measurable item that can be measured directly. <br />
3. values: A quantity might be given as a decimal, range, enumeration or all together. <br />
4. unit: Any measurement unit <br />
5. modifier: The meaning of a quantity is often altered by modifiers such as 'average', 'approx.' <br />

It uses open-ai "chatComletion" API to generate the result. This projects provides two different methods for quantity extraction:
### Single step
Input paragraph is added to a prompt template and asked LLM to generate the result in desired format.
### Multi step
This method generates the results in two steps: <br />
1. NER: It first asks LLM to generate in-line tags for the detected entities. The result of this step is similar to:  <br />
   ```The nominal stack efficiency {{ "measured_property": "nominal stack efficiency" }} of AEL {{ "measured_entity": "AEL" }} and PELEM {{ "measured_entity": "PEMEL" }} is around 63%-71% {{ "quantity_unit": "NOT_DETERMINED", "quantity_upper_value": "71%", quantity_lower_value:"63%", "quantity_modifier": "around"}} and less than 60% {{ "quantity_unit": "NOT_DETERMINED", "quantity_upper_value": "60%", quantity_lower_value:"60%", "quantity_modifier": "less than"}} respectively. ```
2. Relation extraction: The final output generated while the result of previous step added to the prompt template<br />
   <br />
## Output format 
    {{
      "measured_entities": [
          {{
              "entity_name": "<entity_name>",
              "measured_properties": [
                  {{
                      "property_name": "<property_name">",
                      "quantity": {{
                          "quantity_unit": "<quantity_unit>",
                          "quantity_lower_value": "<quantity_lower_value>",
                          "quantity_upper_value": "quantity_upper_value",
                          "quantity_modifier": "<quantity_modifier>"
                      }}
                  }}
              ]
          }}
      ]
    }}
## Install
This project requires python3.9+. To install python packages, enter the below command in project root directory.
```bash
pip install -r requirements.txt
```
## Usage
### Single step
template: 
```py
import engine_single_step
instance = engine_single_step.EngineSingleStep("<open-ai config file>", "<prompt template file>")
results = instance.relation_extractor("<input text>")
```
example:
```py
import engine_single_step
instance = engine_single_step.EngineSingleStep("config_files/openai.yaml", "config_files/prompt_single_step.yaml")
print(instance.relation_extractor(" Old batteries offer about 100-200 Wh/Kg. State of the art batteries offer about 200-400 Wh/Kg."))
```

### Multi step
template:
```py
instance = EngineMultiStep("<open-ai config file>", "<ner prompt template file>", "<prompt template file>")
results = instance.relation_extraction_engine("<input text>")
```
example:
```py
instance = EngineMultiStep("config_files/openai.yaml", "config_files/prompt_ner.yaml", "config_files/prompt_multi_steps.yaml")
print(instance.relation_extraction_engine("The current state of the art batteries offers about 200-400 Wh/Kg (Watt-hours per Kilogram)."))
```

## Config files
All config files are in ```config_files``` folder. <br />
Open-ai API key, model name, top-p, and temprature should be set in ```openai.yaml``` file. <br />
A prompt template of entity recognition: ```prompt_ner.yaml``` file. <br />
A prompt template of single step method: ```prompt_single_step.yaml``` <br />
A prompt template of single step method (open-ai generated prompt):```prompt_single_step_ai_generated.yaml``` <br />
A prompt template of multi step method: ```prompt_multi_steps.yaml``` <br />
## Generating prompt template using LLM
In ```prompt_generation\development_dataset``` folder there are files that contain some training data to be used in prompt generation process.
```bash
cd prompt_generation\
```
```py
import prompt_generation
openai_setting_file = "../config_files/openai.yaml"
prompt_generator = "prompt_generation.yaml"
prompt_relation_extraction = "../config_files/prompt_single_step.yaml"
development_dataset = "development_dataset"
print(prompt_generation.generate_prompt(development_dataset, openai_setting_file, prompt_relation_extraction, prompt_generator))
```

## Evaluation

In ```evaluation``` folder there is a benchmark dataset to be used for evaluation.
```bash
cd evaluation\
```
```py
gold_standard='gold_standard.json'
openai_setting= "../config_files/openai.yaml"
prompt_ner="../config_files/prompt_ner.yaml"
prompt_multi_step= "../config_files/prompt_multi_steps.yaml"
prompt_single_step_ai_generated="../config_files/prompt_single_step_ai_generated.yaml"
prompt_single_step="../config_files/prompt_single_step.yaml"
testing="test_input.json"
#for evaluation multi-step method:
cross_evaluation("evaluation_multi_step.out",openai_setting, gold_standard,testing, prompt_multi_step, prompt_ner, use_multi_step=True )
#for evaluation single-step method:
cross_evaluation("evaluation_single_step.out", openai_setting, gold_standard,testing, prompt_single_step)
#for evaluation single-step method using LLM generated prompt:
cross_evaluation("evaluation_ai_generated_prompt.out", openai_setting, gold_standard,testing, prompt_single_step_ai_generated)
```
## Preprocess

```patent_preprocess.py``` file read a US patent gazette zip file and extract its xml file. Then split the extracted file into json files. Each json file has five fields: patent_name, claim_text, drawing_description, description, and abstract.
```py
import patent_preprocess
zip_file = 'processed_data/ipa210121.zip'
splat_xml = patent_preprocess.load_files(zip_file)
patent_preprocess.preprocess(splat_xml)
```