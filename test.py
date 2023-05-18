import json

def extract_json_from_string(input_string):
    json_start = input_string.find('{')
    json_end = input_string.rfind('}') + 1
    json_string = input_string[json_start:json_end]
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError:
        return None

input_string = 'This is some text. {"name": {"John":"ali"}, "age": 30} Some more text.'
json_object = extract_json_from_string(input_string)
if json_object is not None:
    print(json_object)
else:
    print("No valid JSON found in the input string.")