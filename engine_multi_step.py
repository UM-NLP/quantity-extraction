import openai
import yaml
import json
import spacy
from deepmerge import always_merger

def load_yaml(prompt_file, variable_names):
    with open(prompt_file, 'r', encoding="utf8") as file:
        data_prompt = yaml.safe_load(file)
        for name in variable_names:
            globals()[name] = data_prompt[name] # defining global variables

#load prompt and openai settings
def initialize(setting_file, prompt_ner_file, prompt_multi_step_file):
    variable_names = ['SYSTEM_PROMPT', 'USER_PROMPT', 'ASSISTANT_PROMPT', 'GUIDELINES_PROMPT']
    load_yaml(prompt_multi_step_file, variable_names)
    variable_names = ['SYSTEM_NER_PROMPT', 'USER_NER_PROMPT', 'ASSISTANT_NER_PROMPT', 'GUIDELINES_NER_PROMPT']
    load_yaml(prompt_ner_file, variable_names)
    variable_names = ['MODEL_NAME', 'TOP_P', 'TEMPERATURE', 'API_KEY']
    load_yaml(setting_file, variable_names)
    openai.api_key =API_KEY

def openai_chat_completion_response(system, user, assistance, final):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        top_p= TOP_P,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistance},
            {"role": "user", "content": final}
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
        if len(current_sentence) < 40:
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
def filter_ner_result(input_sentence, ner_output):
    words_str1 = input_sentence.split()
    words_str2 = ner_output.split()
    for i in range(len(words_str2)):
        if words_str2[i:i+len(words_str1)][0] == words_str1[0] and words_str2[i:i+len(words_str1)][1] == words_str1[1]: #compare first two words
            extracted_words = words_str2[i:]
            extracted_sentence = ' '.join(extracted_words)
            return extracted_sentence
    return input_sentence
def relation_extraction_engine(my_sentence):
    sentences=split_text_into_sentences(my_sentence)
    results= {}
    for sentence in sentences:
        try:
            ner_prompt = GUIDELINES_NER_PROMPT.format(sentence)  # inject the input to the ner prompt
            #print("ner_prompt: ", ner_prompt)
            enriched_sentence = openai_chat_completion_response(SYSTEM_NER_PROMPT, USER_NER_PROMPT, ASSISTANT_NER_PROMPT, ner_prompt)  #generate in-line ner
            print (enriched_sentence)
            enriched_sentence=filter_ner_result(sentence,enriched_sentence)
            #print ("ner:  ", enriched_sentence)
            customized_prompt = GUIDELINES_PROMPT.format(enriched_sentence)  # inject the input (including ner) to the prompt
            result_sentence_level = openai_chat_completion_response(SYSTEM_PROMPT, USER_PROMPT, ASSISTANT_PROMPT, customized_prompt)
            result_sentence_level = json.loads(result_sentence_level) #string to json
        except:
            result_sentence_level = {}
        results=always_merger.merge(results, result_sentence_level)
    print (results)
    return results


#initialize("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_ner.yaml", "D:\github\quantity-extraction\prompt_multi_step.yaml")
#relation_extraction_engine("The current state of the art batteries offers about 200-400 Wh/Kg (Watt-hours per Kilogram).")