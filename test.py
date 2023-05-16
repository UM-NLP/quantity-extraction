import json

def calculate_accuracy(data_json, ground_truth_json):
    data = json.loads(data_json)
    ground_truth = json.loads(ground_truth_json)
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
data_json = '''
{"measured": [{
    "name": "Johny",
    "age": 32,
    "address": {
        "street": "123 Main St",
        "city": "London"
    },
    "languages": ["Python", "JavaScript"]
},
{
    "name": "Johny",
    "age": 32,
    "address": {
        "street": "123 Main St",
        "city": "New York"
    },
    "languages": ["Python", "JavaScript"]
}]}
'''

ground_truth_json = '''
{"measured": [{
    "name": "Johnys",
    "age": 32,
    "address": {
        "street": "123 Main St",
        "city": "New York"
    },
    "languages": ["Python", "JavaScript"]
},
{
    "name": "Johny",
    "age": 32,
    "address": {
        "street": "123 Main St",
        "city": "London"
    },
    "languages": ["Pythons", "JavaScript"]
}]}
'''

accuracy = calculate_accuracy(data_json, ground_truth_json)
print(f"Accuracy: {accuracy * 100}%")
