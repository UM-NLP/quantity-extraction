from sklearn.metrics import precision_score, recall_score, f1_score
import json
import sys
sys.path.append("..")  # Add the parent folder to the module search path
from my_dataclass import Patent
import engine_single_step  as relation_extraction_module

def calculate_accuracy(predicted, ground_truth):
    TP=0
    FP=0
    FN=0
    for entity_predicted in predicted['measured_entities']:
        [entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found] = [False] * 6
        for entity_ground in ground_truth['measured_entities']:
            if entity_ground["entity_name"]==entity_predicted["entity_name"]: #measure size of single TP and FP
                entity_found=True
                for property_predicted in entity_predicted["measured_properties"]:
                    for property_ground in entity_ground["measured_properties"]:
                        if property_ground["property_name"] in property_predicted["property_name"]:
                            property_found=True
                            if property_ground["quantity"]["quantity_unit"] in property_predicted["quantity"]["quantity_unit"]:
                                unit_found=True
                            if property_ground["quantity"]["quantity_lower_value"] in property_predicted["quantity"]["quantity_lower_value"]:
                                quantity_lower_found=True
                            if property_ground["quantity"]["quantity_upper_value"] in property_predicted["quantity"]["quantity_upper_value"]:
                                quantity_upper_found=True
                            if property_predicted["quantity"]["quantity_modifier"]:
                                if property_ground["quantity"]["quantity_modifier"] in property_predicted["quantity"]["quantity_modifier"]:
                                    modifier_found=True
        true_count = sum([entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found])
        TP += true_count / 6
        FP += (1 - (true_count / 6))
    for entity_ground in ground_truth['measured_entities']:
        [entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found] = [False] * 6
        for entity_predicted in predicted['measured_entities']:
            if entity_ground["entity_name"]==entity_predicted["entity_name"]: #measure size of single TP and FP
                entity_found=True
            for property_ground in entity_ground["measured_properties"]:
                for property_predicted in entity_predicted["measured_properties"]:
                    if property_ground["property_name"] in property_predicted["property_name"]:
                        property_found=True
                        if property_ground["quantity"]["quantity_unit"] in property_predicted["quantity"]["quantity_unit"]:
                            unit_found=True
                        if property_ground["quantity"]["quantity_lower_value"] in property_predicted["quantity"]["quantity_lower_value"]:
                            quantity_lower_found=True
                        if property_ground["quantity"]["quantity_upper_value"] in property_predicted["quantity"]["quantity_upper_value"]:
                            quantity_upper_found=True
                        if property_predicted["quantity"]["quantity_modifier"]:
                            if property_ground["quantity"]["quantity_modifier"] in property_predicted["quantity"]["quantity_modifier"]:
                                modifier_found=True
        true_count = sum([entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found])
        FN += 1 - (true_count - 1) * 0.15
    precision = TP / (TP + FP)
    recall= TP / (TP + FN)
    f1=2 * (precision * recall) / (precision + recall)
    return f1, precision, recall

#evaluation main function
def evaluate (test_file):
    with open('gold_standard.json', 'r') as file:  # Load the gold standard JSON file
        goldstandard_json = json.load(file)
    #goldstandard_patent = Patent(**goldstandard_json)  # Convert the dictionary to a Patent instance
    with open(test_file, 'r') as file:
        test_input_json = json.load(file)
    #test_patent= Patent(**test_input_json) # Convert the dictionary to a Patent instance
    relation_extraction_module.initialize("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_single_step.yaml")  #tialize relation extraction engine
    predicted_json=relation_extraction_module.relation_extractor(test_input_json["claim_text"])
    #test_patent.measured_entities=predicted_json['measured_entities']
    f1, precision, recall = calculate_accuracy( predicted_json, goldstandard_json)
    output = f"f1: {f1:.4f}, precision: {precision:.4f}, recall: {recall:.4f}"
    with open("evaluation.log", "a") as file:
        file.write(output+"\n")
evaluate ('test_input.json')