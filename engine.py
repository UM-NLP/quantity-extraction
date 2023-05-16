import openai
import yaml
import json
from my_dataclass import MeasuredEntity, MeasuredProperty, Quantity, Patent

# Read the YAML file
with open('prompt_ner.yaml', 'r', encoding="utf8") as file:
    data = yaml.safe_load(file)

# Access the elements
SYSTEM_PROMPT = data['SYSTEM_PROMPT']
USER_PROMPT_1 = data['USER_PROMPT_1']
ASSISTANT_PROMPT_1 = data['ASSISTANT_PROMPT_1']
GUIDELINES_PROMPT = data['GUIDELINES_PROMPT']

# Set openai.api_key to the OPENAI environment variable
openai.api_key = "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"

def openai_chat_completion_response(final_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        top_p= 0,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_1},
            {"role": "assistant", "content": ASSISTANT_PROMPT_1},
            {"role": "user", "content": final_prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip(" \n")

my_sentence = "Based on the above description, in the design of the package structure of the disclosure, the circuit board includes the composite material layer with a thermal conductivity between 450 W/mK and 700 W/mK, and the heat generated by the heat generating element may be transferred to the external environment through the composite material layer. The current state of the art batteries offers about 200-400 Wh/Kg (Watt-hours per Kilogram).  A thermal conductivity of the composite material layer is between 450 W/mK and 700 W/mK. The heat generating element is disposed on the circuit board and electrically connected to the circuit layers. Heat generated by the heat generating element is transmitted to an external environment through the composite material layer. A package structure including a circuit board and a heat generating element is provided. The circuit board includes a plurality of circuit layers and a composite material layer. A thermal conductivity of the composite material layer is between 450 W/mK and 700 W/mK. The heat generating element is disposed on the circuit board and electrically connected to the circuit layers. Heat generated by the heat generating element is transmitted to an external environment through the composite material layer. "
GUIDELINES_PROMPT = GUIDELINES_PROMPT.format(my_sentence)
ners = openai_chat_completion_response(GUIDELINES_PROMPT)
print(ners)
# import re
# pattern_entities = r'measured_entities= (\[{[^}]+}\])'
# pattern_properties = r'measured_properties= (\[{[^}]+}\])'
# pattern_quantities = r'quantities= (\[{[^}]+}\])'
# match_entities = re.search(pattern_entities, ners)
# match_properties = re.search(pattern_properties, ners)
# match_quantities = re.search(pattern_quantities, ners)
# if match_entities:
#     entities_str = match_entities.group(1)
#     entities_json = json.loads(entities_str)
#     entities_list = [MeasuredEntity(**data) for data in entities_json]
# if match_properties:
#     properties_str = match_properties.group(1)
#     properties_json = json.loads(properties_str)
#     properties_list = [MeasuredProperty(**data) for data in properties_json]
# if match_quantities:
#     quantities_str = match_quantities.group(1)
#     quantities_json = json.loads(quantities_str)
#     quantities_list = [Quantity(**data) for data in quantities_json]
#
#
#
# # Create a list of MeasuredEntity instances
#
#
# # Print the list of instances
# for entity in entities_list:
#     print(entity)
# # Print the list of instances
# for entity in properties_list:
#     print(entity)
#     # Print the list of instances
# for entity in quantities_list:
#     print(entity)
