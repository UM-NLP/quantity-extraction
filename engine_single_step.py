import openai
import yaml
import json
import spacy
from deepmerge import always_merger
SENTENCE_THRESHOLD=40  # minimum number of characters per sentence
class EngineSingleStep:

    def load_yaml(self, prompt_file, variable_names): # read yaml file into variables
        with open(prompt_file, 'r', encoding="utf8") as file:
            data_prompt = yaml.safe_load(file)
            for name in variable_names:
                setattr(self, name, data_prompt[name]) # runtime variable creation

    def __init__(self, setting_file, prompt):
        global spacy_engine
        spacy_engine = spacy.load("en_core_web_sm")
        variable_names = ['SYSTEM_PROMPT', 'USER_PROMPT', 'ASSISTANT_PROMPT', 'GUIDELINES_PROMPT'] # prompt portions
        self.load_yaml(prompt, variable_names)
        variable_names = ['MODEL_NAME', 'TOP_P', 'TEMPERATURE', 'API_KEY'] # open-ai settings
        self.load_yaml(setting_file, variable_names)
        openai.api_key =self.API_KEY

    def openai_chat_completion_response( self, final_prompt):
        response = openai.ChatCompletion.create(
            model=self.MODEL_NAME, # hyperparameters
            top_p= self.TOP_P,
            temperature=self.TEMPERATURE,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT}, # template prompt
                {"role": "user", "content": self.USER_PROMPT}, # template prompt
                {"role": "assistant", "content": self.ASSISTANT_PROMPT}, # template prompt
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

    def json_validator(self, text):
        text=text.replace("Output: ","").replace("System output:","").strip() # remove unnecessary phrases
        json_start = text.find('{') # find first occurrence of {
        json_end = text.rfind('}') + 1 # find the last occurrence of }
        json_string = text[json_start:json_end]
        try:
            json_object = json.loads(json_string)
            return json_object
        except json.JSONDecodeError:
            return None

    def relation_extractor(self, my_sentence):
        sentences=self.split_text_into_sentences(my_sentence)
        results= {}
        for sentence in sentences:
            try:
                customized_prompt = self.GUIDELINES_PROMPT.format(sentence)  # inject the input to the prompt
                result_sentence_level = self.openai_chat_completion_response(customized_prompt)  #extract information
                result_sentence_level=self.json_validator(result_sentence_level) #string to json
            except:
                result_sentence_level = None
            if result_sentence_level:
                results=always_merger.merge(results, result_sentence_level) # merge two json objects
        return results