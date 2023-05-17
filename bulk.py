import json
import os
import engine_single_step  as relation_extraction_module

relation_extraction_module.initialize("D:\github\quantity-extraction\openai.yaml", "D:\github\quantity-extraction\prompt_single_step.yaml")  #tialize relation extraction engine
def process_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            # Read the JSON file
            with open(file_path, "r",encoding='utf-8') as file:
                json_data = json.load(file )
            # Process the JSON data using the relation_extraction_engine function
            result = relation_extraction_module.relation_extractor(json_data["claim_text"])
            # Create a new file with the same name and write the result as JSON
            result_file_path = os.path.join(folder_path, f"result_{filename}")
            with open(result_file_path, "w", encoding='utf-8') as result_file:
                json.dump(result, result_file, indent=4, ensure_ascii=False)
            print(f"Processed file: {filename}")
    print("All files processed successfully.")

# Provide the folder path containing the JSON files
folder_path = "D:\github\quantity-extractor\data"

# Call the process_json_files function
process_json_files(folder_path)
