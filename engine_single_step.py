import openai
import yaml
import json
import spacy
from deepmerge import always_merger
#readimg yml file into variables
def load_yaml(prompt_file, variable_names):
    with open(prompt_file, 'r', encoding="utf8") as file:
        data_prompt = yaml.safe_load(file)
        for name in variable_names:
            globals()[name] = data_prompt[name]

#load prompt, spacy model, and openai settings
def initialize(setting_file, prompt_multi_step_file):
    global nlp
    nlp = spacy.load("en_core_web_sm")
    variable_names = ['SYSTEM_PROMPT', 'USER_PROMPT', 'ASSISTANT_PROMPT', 'GUIDELINES_PROMPT']
    load_yaml(prompt_multi_step_file, variable_names)
    variable_names = ['MODEL_NAME', 'TOP_P', 'TEMPERATURE', 'API_KEY']
    load_yaml(setting_file, variable_names)
    openai.api_key =API_KEY

def openai_chat_completion_response( final_prompt):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        top_p= TOP_P,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": ASSISTANT_PROMPT},
            {"role": "user", "content": final_prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip(" \n")
# The function checks if the length of the current sentence (including any previous sentences) is less than 100 characters.
# If it is, the current sentence is added to the previous sentence with a space in between.
# Otherwise, the current sentence is considered as a new separate sentence.
def split_text_into_sentences(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = []
    current_sentence = ""
    for sentence in doc.sents:
        if len(current_sentence) < 100:
            if current_sentence:
                current_sentence += " " + sentence.text
            else:
                current_sentence += sentence.text
        else:
            sentences.append(current_sentence)
            current_sentence = sentence.text
    if current_sentence:
        sentences.append(current_sentence)
    return sentences

def relation_extraction_engine(my_sentence):
    sentences=split_text_into_sentences(my_sentence)
    results= {}
    #merger = Merger([(list, "append")], [], [])
    for sentence in sentences:
        try:
            customized_prompt = GUIDELINES_PROMPT.format(sentence)  # inject the input to the prompt
            result_sentence_level = openai_chat_completion_response(customized_prompt)  #extract informatio
            result_sentence_level = json.loads(result_sentence_level) #string to json
        except:
            result_sentence_level = {}
        results=always_merger.merge(results, result_sentence_level)
    print (results)
    return results
# initialize("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_single_step.yaml")
# relation_extraction_engine(" Old batteries offer about 100-200 Wh/Kg. State of the art batteries offer about 200-400 Wh/Kg.")