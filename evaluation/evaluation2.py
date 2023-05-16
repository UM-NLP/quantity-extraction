from sklearn.metrics import precision_score, recall_score, f1_score
import json
import sys
sys.path.append("..")  # Add the parent folder to the module search path
from my_dataclass import Patent
import engine_multi_step  as relation_extraction_module

def calculate_accuracy(data, ground_truth):
    total_keys = 0
    matching_keys = 0
    def iterate_keys(obj1, obj2):
        nonlocal total_keys, matching_keys
        if isinstance(obj1, dict) and isinstance(obj2, dict):
            for key in obj1.keys():
                total_keys += 1
                if key in obj2 and obj1[key] == obj2[key]:
                    matching_keys += 1
                elif key in obj1 and key in obj2:
                    iterate_keys(obj1[key], obj2[key])
        elif isinstance(obj1, list) and isinstance(obj2, list):
            for item1, item2 in zip(obj1, obj2):
                iterate_keys(item1, item2)
    iterate_keys(data, ground_truth)
    accuracy = matching_keys / total_keys
    return accuracy


#evaluation main function
def evaluate (test_file):
    with open('gold_standard.json', 'r') as file:  # Load the gold standard JSON file
        goldstandard_json = json.load(file)
    #goldstandard_patent = Patent(**goldstandard_json)  # Convert the dictionary to a Patent instance
    with open(test_file, 'r') as file:
        test_input_json = json.load(file)
    #test_patent= Patent(**test_input_json) # Convert the dictionary to a Patent instance
    relation_extraction_module.initialize("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_ner.yaml", "D:\github\quantity-extraction\prompt_multi_step.yaml")  #tialize relation extraction engine
    predicted_json=relation_extraction_module.relation_extraction_engine(test_input_json["claim_text"])
    #test_patent.measured_entities=predicted_json['measured_entities']
    precision, recall, f1_score = calculate_accuracy( predicted_json, goldstandard_json)  # passing testig data and the benchmark
    with open("evaluation2.log", "a") as file:
        file.write(f"Precision: {precision}\nRecall: {recall}\nF1 Score: {f1_score}\n")
evaluate ('test_input.json')