import os
import json
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize
import spacy
# Folder path containing the JSON files
folder_path = "D:\\github\\quantity-extraction\\data"
# Fields to analyze
fields = ['claim_text', 'drawing_description', 'description', 'abstract']
# Initialize NLP models
nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')

# Function to extract quantitative data and measurement information from a text
def extract_quantitative_data(text):
    doc = nlp(text)
    quantitative_data = []

    # Extract numerical values and measurement units
    for ent in doc.ents:
        if ent.label_ in ['QUANTITY', 'DATE', 'TIME', 'PERCENT', 'MONEY']:
            quantitative_data.append(ent.text)

    return quantitative_data

# Initialize accumulated results for all JSON files
accumulated_results = {field: {'text': '', 'scores': []} for field in fields}

# Analyze each JSON file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)

        # Load the JSON file
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)

        # Analyze each field
        for field in fields:
            text = data.get(field, '')
            accumulated_results[field]['text'] += text

            # Split the text into sentences
            sentences = sent_tokenize(text)

            # Analyze each sentence
            sentence_scores = []
            for sentence in sentences:
                quantitative_data = extract_quantitative_data(sentence)
                sentence_scores.append(len(quantitative_data))

            # Append the scores to the accumulated results
            accumulated_results[field]['scores'].extend(sentence_scores)

# Calculate average scores for each field
for field in fields:
    scores = accumulated_results[field]['scores']
    avg_score = sum(scores) / len(scores)
    accumulated_results[field]['avg_score'] = avg_score

# Plotting the results
plt.figure(figsize=(12, 6))

for i, field in enumerate(fields, start=1):
    plt.subplot(2, 2, i)
    scores = accumulated_results[field]['scores']
    plt.plot(scores)
    plt.xlabel('Sentence Index')
    plt.ylabel('Quantitative Data Count')
    plt.title(f'{field} - Avg Score: {accumulated_results[field]["avg_score"]:.2f}')

plt.tight_layout()
plt.show()
