import openai
import yaml
import spacy

class LlmEngine:

    def load_yaml(self, prompt_file, variable_names): # read yml file into variables
        with open(prompt_file, 'r', encoding="utf8") as file:
            data_prompt = yaml.safe_load(file)
            for name in variable_names:
                setattr(self, name, data_prompt[name])

    def __init__(self, setting_file, prompt): # load prompt, spacy model, and openai settings
        global nlp
        nlp = spacy.load("en_core_web_sm")
        variable_names = ['SYSTEM_PROMPT', 'USER_PROMPT', 'ASSISTANT_PROMPT', 'GUIDELINES_PROMPT']
        self.load_yaml(prompt, variable_names)
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
            customized_prompt = self.GUIDELINES_PROMPT.format(intput, current_re_prompt)  # inject the input to the prompt
            result = self.openai_chat_completion_response(customized_prompt)  #generate new re prompt
        except:
            print("exception")
            result = current_re_prompt
        return result