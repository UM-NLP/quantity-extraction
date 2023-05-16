from sklearn.metrics import precision_score, recall_score, f1_score
import json
import sys
sys.path.append("..")  # Add the parent folder to the module search path
from my_dataclass import Patent
import engine_single_step  as relation_extraction_module
def calculate_metrics(gold_standard, predicted_result):
    true_labels = []
    predicted_labels = []
    for gold_entity in gold_standard.measured_entities: # Iterate over the gold standard measured entities
        entity_name = gold_entity["entity_name"]
        gold_relations = gold_entity["measured_properties"]
        predicted_entity = next((p_entity for p_entity in predicted_result.measured_entities if p_entity["entity_name"] == entity_name), None)  # Find the corresponding predicted entity
        if predicted_entity is not None:
            for gold_relation in gold_relations: # Compare the relations of the gold standard and predicted entities
                relation_name = gold_relation["property_name"]
                gold_quantity = gold_relation["quantity"]
                predicted_relation = next((p_relation for p_relation in predicted_entity["measured_properties"] if p_relation["property_name"] == relation_name), None) # Find the corresponding predicted relation
                if predicted_relation is not None:
                    predicted_quantity = predicted_relation["quantity"]  # Compare the quantity values
                    if gold_quantity == predicted_quantity:
                        true_labels.append(1)  # True positive
                        predicted_labels.append(1)
                    else:
                        true_labels.append(1)  # False negative
                        predicted_labels.append(0)
                else:
                    true_labels.append(1)  # False negative
                    predicted_labels.append(0)
        else:
            true_labels.extend([1] * len(gold_relations))  # False negative
            predicted_labels.extend([0] * len(gold_relations))
    # Calculate precision, recall, and F1 score
    precision = precision_score(true_labels, predicted_labels)
    recall = recall_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels)
    return precision, recall, f1
#evaluation main function
def evaluate (test_file):
    with open('gold_standard.json', 'r') as file:  # Load the gold standard JSON file
        goldstandard_json = json.load(file)
    goldstandard_patent = Patent(**goldstandard_json)  # Convert the dictionary to a Patent instance
    with open(test_file, 'r') as file:
        test_input_json = json.load(file)
    test_patent= Patent(**test_input_json) # Convert the dictionary to a Patent instance
    relation_extraction_module.initialize("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_single_step.yaml")  #tialize relation extraction engine
    predicted_json=relation_extraction_module.relation_extraction_engine(test_patent.claim_text)
    test_patent.measured_entities=predicted_json['measured_entities']
    precision, recall, f1_score = calculate_metrics(goldstandard_patent, test_patent)  # passing testig data and the benchmark
    with open("evaluation.log", "a") as file:
        file.write(f"Precision: {precision}\nRecall: {recall}\nF1 Score: {f1_score}\n")
evaluate ('test_input.json')