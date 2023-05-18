import os
import json
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize
import spacy
# Folder path containing the JSON files
folder_path = "processed_data"
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
def process_files(folder_path, fields, n):
    count = 0  # Counter for processed files
    for filename in os.listdir(folder_path):
        if count >= n:
            break
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            # Load the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for field in fields: # Analyze each field
                text = data.get(field, '')
                accumulated_results[field]['text'] += text
                sentences = sent_tokenize(text) # Split the text into sentences
                sentence_scores = [] # Analyze each sentence
                for sentence in sentences:
                    quantitative_data = extract_quantitative_data(sentence)
                    sentence_scores.append(len(quantitative_data))
                # Append the scores to the accumulated results
                accumulated_results[field]['scores'].extend(sentence_scores)
            count += 1  # Increment the counter
    return accumulated_results
accumulated_results=process_files(folder_path, fields, 100)
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
