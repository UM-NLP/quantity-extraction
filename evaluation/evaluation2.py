import json
import sys
import engine_multi_step
import engine_single_step
sys.path.append("..")  # Add the parent folder to the module search path

def calculate_accuracy(predicted, ground_truth):
    tp=0
    fp=0
    fn=0
    for entity_predicted in predicted['measured_entities']:
        [entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found] = [False] * 6
        for entity_ground in ground_truth['measured_entities']:
            if "entity_name" in  entity_predicted:
                if entity_predicted["entity_name"] in entity_ground["entity_name"]: #measure size of single TP and FP
                    entity_found=True
                for property_predicted in entity_predicted["measured_properties"]:
                    for property_ground in entity_ground["measured_properties"]:
                        if property_predicted["property_name"] in property_ground["property_name"]:
                            property_found=True
                            if property_predicted["quantity"]["quantity_unit"] in property_ground["quantity"]["quantity_unit"] :
                                unit_found=True
                            if property_predicted["quantity"]["quantity_lower_value"] in property_ground["quantity"]["quantity_lower_value"] :
                                quantity_lower_found=True
                            if property_predicted["quantity"]["quantity_upper_value"] in property_ground["quantity"]["quantity_upper_value"]:
                                quantity_upper_found=True
                            if property_predicted["quantity"]["quantity_modifier"] in property_ground["quantity"]["quantity_modifier"]:
                                modifier_found=True
        true_count = sum([entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found])
        tp += true_count / 6
        fp += (1 - (true_count / 6))
    for entity_ground in ground_truth['measured_entities']:
        [entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found] = [False] * 6
        for entity_predicted in predicted['measured_entities']:
            if "entity_name" in  entity_predicted:
                if entity_predicted["entity_name"] in entity_ground["entity_name"]: #measure size of single TP and FP
                    entity_found=True
            for property_ground in entity_ground["measured_properties"]:
                for property_predicted in entity_predicted["measured_properties"]:
                    if  property_predicted["property_name"] in property_ground["property_name"]:
                        property_found=True
                        if property_predicted["quantity"]["quantity_unit"] in property_ground["quantity"]["quantity_unit"]:
                            unit_found=True
                        if  property_predicted["quantity"]["quantity_lower_value"] in property_ground["quantity"]["quantity_lower_value"]:
                            quantity_lower_found=True
                        if property_predicted["quantity"]["quantity_upper_value"] in property_ground["quantity"]["quantity_upper_value"]:
                            quantity_upper_found=True
                        if property_predicted["quantity"]["quantity_modifier"] in property_ground["quantity"]["quantity_modifier"]:
                            modifier_found=True
        true_count = sum([entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found])
        fn += 1 - (true_count - 1) * 0.15
    precision = tp / (tp+ fp)
    recall= tp / (tp + fn)
    f1=2 * (precision * recall) / (precision + recall)
    return f1, precision, recall

def cross_evaluation_single_method(openai_setting, gold_standard_file, test_file, prompt_single_step):
    engine_single_step.initialize(openai_setting, prompt_single_step)  #tialize single-step relation extraction engine
    total_precision=total_recall=total_f1=0
    with open("evaluation_single_step.log", "a") as output_handle, open(gold_standard_file, 'r') as gold_standard_handle, open(test_file, 'r') as test_file_handle:  # Load the gold standard JSON file
        goldstandard_json = json.load(gold_standard_handle)
        test_input_json = json.load(test_file_handle)
        for i in range(0, iteration):
            f1, precision, recall=calculate_accuracy(engine_single_step.relation_extractor(test_input_json["claim_text"]), goldstandard_json)
            total_f1, total_precision, total_recall = total_f1 + f1, total_precision + precision, total_recall+ recall
            output_handle.write(f"ROUND {i} (single-step): f1: {f1:.2f}, precision: {precision:.2f}, recall: {recall:.2f}\n")
        output_handle.write(f"(SINGLE-STEP) average f1: {total_f1/iteration:.4f}, average precision: {total_precision/iteration:.4f}, average recall: {total_recall/iteration:.4f}")

def cross_evaluation_multi_method(openai_setting, gold_standard_file, test_file, prompt_ner, prompt_multi_step):
    engine_multi_step.initialize(openai_setting, prompt_ner, prompt_multi_step)  #tialize multi-step relation extraction engine
    total_precision=total_recall=total_f1=0
    with open("evaluation_multi_step.log", "a") as output_handle, open(gold_standard_file, 'r') as gold_standard_handle, open(test_file, 'r') as test_file_handle:  # Load the gold standard JSON file
        goldstandard_json = json.load(gold_standard_handle)
        test_input_json = json.load(test_file_handle)
        for i in range(0, iteration):
            f1, precision, recall=calculate_accuracy(engine_multi_step.relation_extraction_engine(test_input_json["claim_text"]), goldstandard_json)
            total_f1, total_precision, total_recall = total_f1 + f1, total_precision + precision, total_recall + recall
            output_handle.write(f"ROUND {i} (multi-step): f1: {f1:.2f}, precision: {precision:.2f}, recall: {recall:.2f}\n")
        output_handle.write(f"(MULTI-STEP) average f1: {total_f1/iteration:.4f}, average precision: {total_precision/iteration:.4f}, average recall: {total_recall/iteration:.4f}")

gold_standard_file='gold_standard.json'
openai_setting_file="../openai.yaml"
prompt_ner_file="../prompt_ner2.yaml"
prompt_multi_step_file="../prompt_multi_steps.yaml"
prompt_single_step_file="../prompt_single_step.yaml"
testing_file="test_input.json"
iteration=10
cross_evaluation_multi_method(openai_setting_file, gold_standard_file,testing_file, prompt_ner_file, prompt_multi_step_file )
cross_evaluation_single_method(openai_setting_file, gold_standard_file,testing_file, prompt_single_step_file )