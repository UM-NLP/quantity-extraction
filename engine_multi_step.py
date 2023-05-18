import openai
import yaml
import json
import spacy
from deepmerge import always_merger
SENTENCE_THRESHOLD=40  # minimum number of characters per sentence

class EngineMultiStep:
    def load_yaml(self, prompt_file, variable_names): # read yaml file into variables
        with open(prompt_file, 'r', encoding="utf8") as file:
            data_prompt = yaml.safe_load(file)
            for name in variable_names:
                setattr(self, name, data_prompt[name]) # runtime variable creation

    #load prompt and openai settings
    def __init__(self, setting_file, prompt_ner_file, prompt_multi_step_file): #load ner and re prompts, spacy model, and openai settings
        global spacy_engine
        spacy_engine = spacy.load("en_core_web_sm")
        variable_names = ['SYSTEM_PROMPT', 'USER_PROMPT', 'ASSISTANT_PROMPT', 'GUIDELINES_PROMPT']
        self.load_yaml(prompt_multi_step_file, variable_names)
        variable_names = ['SYSTEM_NER_PROMPT', 'USER_NER_PROMPT', 'ASSISTANT_NER_PROMPT', 'GUIDELINES_NER_PROMPT'] # prompt portions
        self.load_yaml(prompt_ner_file, variable_names)
        variable_names = ['MODEL_NAME', 'TOP_P', 'TEMPERATURE', 'API_KEY'] # open-ai settings
        self.load_yaml(setting_file, variable_names)
        openai.api_key =self.API_KEY

    def openai_chat_completion_response(self, system_prompt, user_prompt, assistant_prompt, final_prompt):
        response = openai.ChatCompletion.create(
            model=self.MODEL_NAME,
            top_p= self.TOP_P,
            temperature=self.TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt}, # template prompt
                {"role": "user", "content": user_prompt}, # template prompt
                {"role": "assistant", "content": assistant_prompt}, # template prompt
                {"role": "user", "content": final_prompt} # input injected prompt
            ]
        )
        return response['choices'][0]['message']['content'].strip(" \n")

    # An Spacy sentence detection. The function also checks if the length of the current sentence is very short.
    # If it is, the current sentence is added to the previous sentence with a space in between.
    def split_text_into_sentences(self, text):
        doc = spacy_engine(text)
        sentences = []
        current_sentence = ""
        for sentence in doc.sents:
            if len(current_sentence) < SENTENCE_THRESHOLD: # less than minimum number of characters per sentence
                if current_sentence:
                    current_sentence += " " + sentence.text
                else:
                    current_sentence += sentence.text
            else:
                sentences.append(current_sentence)
                current_sentence = sentence.text
        if len(current_sentence) > SENTENCE_THRESHOLD: # the last sentence special case
            sentences.append(current_sentence)
        return sentences
    def filter_ner_result(self, input_sentence, ner_output):
        words_str1 = input_sentence.split()
        words_str2 = ner_output.split()
        for i in range(len(words_str2)):
            if words_str2[i:i+len(words_str1)][0] == words_str1[0] and words_str2[i:i+len(words_str1)][1] == words_str1[1]: #compare first two words
                extracted_words = words_str2[i:]
                extracted_sentence = ' '.join(extracted_words)
                return extracted_sentence
        return input_sentence
    def relation_extraction_engine(self, my_sentence):
        sentences=self.split_text_into_sentences(my_sentence)
        results= {}
        for sentence in sentences:
            try:
                ner_prompt = self.GUIDELINES_NER_PROMPT.format(sentence)  # inject the input to the ner prompt
                #print("ner_prompt: ", ner_prompt)
                enriched_sentence = self.openai_chat_completion_response(self.SYSTEM_NER_PROMPT, self.USER_NER_PROMPT, self.ASSISTANT_NER_PROMPT, ner_prompt)  #generate in-line ner
                enriched_sentence=self.filter_ner_result(sentence,enriched_sentence)
                #print ("ner:  ", enriched_sentence)
                customized_prompt = self.GUIDELINES_PROMPT.format(enriched_sentence)  # inject the input (including ner) to the prompt
                result_sentence_level = self.openai_chat_completion_response(self.SYSTEM_PROMPT, self.USER_PROMPT, self.ASSISTANT_PROMPT, customized_prompt)
                result_sentence_level = json.loads(result_sentence_level) #string to json
            except:
                result_sentence_level = {}
            results=always_merger.merge(results, result_sentence_level)
        return results