import openai
import yaml
import json
import spacy
from deepmerge import always_merger

class EngineSingleStep:
    #readimg yml file into variables
    def load_yaml(self, prompt_file, variable_names):
        with open(prompt_file, 'r', encoding="utf8") as file:
            data_prompt = yaml.safe_load(file)
            for name in variable_names:
                setattr(self, name, data_prompt[name])


    #load prompt, spacy model, and openai settings
    def __init__(self, setting_file, prompt_multi_step_file):
        global nlp
        nlp = spacy.load("en_core_web_sm")
        variable_names = ['SYSTEM_PROMPT', 'USER_PROMPT', 'ASSISTANT_PROMPT', 'GUIDELINES_PROMPT']
        self.load_yaml(prompt_multi_step_file, variable_names)
        variable_names = ['MODEL_NAME', 'TOP_P', 'TEMPERATURE', 'API_KEY']
        self.load_yaml(setting_file, variable_names)
        openai.api_key =self.API_KEY

    def openai_chat_completion_response( self, final_prompt):
        response = openai.ChatCompletion.create(
            model=self.MODEL_NAME,
            top_p= self.TOP_P,
            temperature=self.TEMPERATURE,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": self.USER_PROMPT},
                {"role": "assistant", "content": self.ASSISTANT_PROMPT},
                {"role": "user", "content": final_prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip(" \n")
    # An Spacy sentence detection. The function also checks if the length of the current sentence is very short.
    # If it is, the current sentence is added to the previous sentence with a space in between.
    def split_text_into_sentences(self, text):
        THRESHOLD=40
        doc = nlp(text)
        sentences = []
        current_sentence = ""
        for sentence in doc.sents:
            if len(current_sentence) < THRESHOLD:
                if current_sentence:
                    current_sentence += " " + sentence.text
                else:
                    current_sentence += sentence.text
            else:
                sentences.append(current_sentence)
                current_sentence = sentence.text
        if len(current_sentence) > THRESHOLD:
            sentences.append(current_sentence)
        return sentences
    def json_validator(self, text):
        text=text.replace("Output: ","").strip()
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        json_string = text[json_start:json_end]
        try:
            json_object = json.loads(json_string)
            return json_object
        except json.JSONDecodeError:
            return None
        json_text = json.loads(text)
        return json_text

    def relation_extractor(self, my_sentence):
        sentences=self.split_text_into_sentences(my_sentence)
        results= {}
        for sentence in sentences:
            #try:
                customized_prompt = self.GUIDELINES_PROMPT.format(sentence)  # inject the input to the prompt
                #customized_prompt=customized_prompt.replace("{{","{").replace("}}","}")
                result_sentence_level = self.openai_chat_completion_response(customized_prompt)  #extract informatio
                result_sentence_level=self.json_validator(result_sentence_level) #string to json
            #except:
                #result_sentence_level = {}
                results=always_merger.merge(results, result_sentence_level)
        return results
    def select_prompt(self, chatbot_output):
        start_marker = r"Entity Definitions"
        end_marker = r"}"
        start_index = chatbot_output.find(start_marker)
        end_index = chatbot_output.rfind(end_marker)
        if start_index == -1:
            start_index = chatbot_output.find("Please provide")
        if start_index != -1 and end_index != -1:
            end_index += len(end_marker)
            selected_part = chatbot_output[start_index:end_index]
            selected_part=selected_part.replace("{","{{").replace("}","}}")
            selected_part+="\n Sentence: {} \n Output: "
            return selected_part
        else:
            chatbot_output

    def prompt_generator(self, intput, current_re_prompt ):
        try:
            #current_re_prompt=current_re_prompt.format(" {} ")
            customized_prompt = self.GUIDELINES_PROMPT.format(intput, current_re_prompt)  # inject the input to the prompt
            result = self.openai_chat_completion_response(customized_prompt)  #generate new re prompt
            #new_re_prompt=self.select_prompt(result)
        except:
            print("exception")
            result = current_re_prompt
        return result
# instance=EngineSingleStep("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_single_step.yaml")
# instance.relation_extractor(" Old batteries offer about 100-200 Wh/Kg. State of the art batteries offer about 200-400 Wh/Kg.")