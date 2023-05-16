import json
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize
import spacy
# Load the JSON file
with open('D:\\github\\quantity-extraction\\data\\US-20210000003-A1.json', 'r') as file:
    data = json.load(file)
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
# Analyze each field
results = {}
for field in fields:
    text = data.get(field, '')
    # Split the text into sentences
    sentences = sent_tokenize(text)
    # Analyze each sentence
    sentence_scores = []
    for sentence in sentences:
        quantitative_data = extract_quantitative_data(sentence)
        sentence_scores.append(len(quantitative_data))
    # Store the analysis results
    results[field] = {
        'text': text,
        'scores': sentence_scores,
        'avg_score': sum(sentence_scores) / len(sentence_scores)
    }
# Plotting the results
plt.figure(figsize=(12, 6))
for i, field in enumerate(fields, start=1):
    plt.subplot(2, 2, i)
    scores = results[field]['scores']
    plt.plot(scores)
    plt.xlabel('Sentence Index')
    plt.ylabel('Quantitative Data Count')
    plt.title(f'{field} - Avg Score: {results[field]["avg_score"]:.2f}')
plt.tight_layout()
plt.show()
