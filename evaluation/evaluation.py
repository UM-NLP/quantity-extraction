import json
import sys
sys.path.append("..") # Add the parent folder to the module search path
import engine_multi_step
import engine_single_step
ITERATION=10 # number of evaluation iterations
def calculate_tp_fp(predicted, ground_truth):
    tp = 0
    fp = 0

    for entity_predicted in predicted['measured_entities']:
        for entity_ground in ground_truth['measured_entities']:
            if "entity_name" in entity_predicted and entity_predicted["entity_name"] in entity_ground["entity_name"]:
                entity_found = True
                for property_predicted in entity_predicted["measured_properties"]:
                    for property_ground in entity_ground["measured_properties"]:
                        if property_predicted["property_name"] in property_ground["property_name"]:
                            property_found = True
                            quantity = property_predicted.get("quantity", {})
                            quantity_ground = property_ground.get("quantity", {})
                            unit_found = quantity.get("quantity_unit") == quantity_ground.get("quantity_unit")
                            quantity_lower_found = quantity.get("quantity_lower_value") == quantity_ground.get("quantity_lower_value")
                            quantity_upper_found = quantity.get("quantity_upper_value") == quantity_ground.get("quantity_upper_value")
                            modifier_found = quantity.get("quantity_modifier") == quantity_ground.get("quantity_modifier")

                            true_count = sum([entity_found, property_found, unit_found, quantity_lower_found, quantity_upper_found, modifier_found])
                            tp += true_count / 6
                            fp += (1 - (true_count / 6))

    return tp, fp

def calculate_fn(predicted, ground_truth):
    fn = 0
    for entity_ground in ground_truth['measured_entities']:
        true_count = 0
        for entity_predicted in predicted['measured_entities']:
            if entity_predicted.get("entity_name", "") in entity_ground.get("entity_name", ""):
                true_count += 1
            for property_ground in entity_ground.get("measured_properties", []):
                for property_predicted in entity_predicted.get("measured_properties", []):
                    if property_predicted.get("property_name", "") in property_ground.get("property_name", ""):
                        true_count += 1
                        predicted_quantity = property_predicted.get("quantity", {})
                        ground_quantity = property_ground.get("quantity", {})
                        if predicted_quantity.get("quantity_unit", "") == ground_quantity.get("quantity_unit", ""):
                            true_count += 1
                        if predicted_quantity.get("quantity_lower_value", "") == ground_quantity.get("quantity_lower_value", ""):
                            true_count += 1
                        if predicted_quantity.get("quantity_upper_value", "") == ground_quantity.get("quantity_upper_value", ""):
                            true_count += 1
                        if predicted_quantity.get("quantity_modifier", "") == ground_quantity.get("quantity_modifier", ""):
                            true_count += 1
        fn += 1 - (true_count - 1) * 0.15
    return fn

def calculate_f1(predicted, ground_truth):
    tp, fp=calculate_tp_fp(predicted, ground_truth) # count true positives and false positives
    fn=calculate_fn(predicted, ground_truth) # count false negatives
    precision = tp / (tp+ fp)
    recall= tp / (tp + fn)
    f1=2 * (precision * recall) / (precision + recall)
    return f1, precision, recall
def cross_evaluation(output_file, openai_setting, gold_standard_file, test_file, prompt, prompt_ner=None, use_multi_step=False):
    if use_multi_step: # Initialize the multi-step relation extraction engine
        relation_extractor = engine_multi_step.EngineMultiStep(openai_setting, prompt_ner, prompt)
        step_type = "MULTI-STEP"
    else: # Initialize the single-step relation extraction engine
        relation_extractor = engine_single_step.EngineSingleStep(openai_setting, prompt)
        step_type = "SINGLE-STEP"
    total_precision = total_recall = total_f1 = 0
    with open(output_file, "a") as output_handle, open(gold_standard_file, 'r') as gold_standard_handle, open(test_file, 'r') as test_file_handle:
        goldstandard_json = json.load(gold_standard_handle)
        test_input_json = json.load(test_file_handle)
        for i in range(ITERATION):
            result = relation_extractor.relation_extractor(test_input_json["claim_text"])
            f1, precision, recall = calculate_f1(result, goldstandard_json)
            total_f1 += f1
            total_precision += precision
            total_recall += recall
            output_handle.write("input text: " + str(test_input_json["claim_text"]) + "\n" + "result: " + str(result)+ "\n") # log the input and output
            output_handle.write(f"ROUND {i} ({step_type}): f1: {f1:.2f}, precision: {precision:.2f}, recall: {recall:.2f}\n")
        output_handle.write(f"({step_type}) average f1: {total_f1 / ITERATION:.4f}, average precision: {total_precision / ITERATION:.4f}, average recall: {total_recall / ITERATION:.4f}")

