import matplotlib.pyplot as plt
import spacy
import os
import json
def extract_quantitative_data(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    quantitative_data = []
    # Extract numerical values and measurement units
    for ent in doc.ents:
        if ent.label_ in ['QUANTITY', 'DATE', 'TIME', 'PERCENT', 'MONEY']:
            quantitative_data.append(ent.text)
    return quantitative_data

def count_quantitative_data(paragraphs):
    sentence_counts = []
    for paragraph in paragraphs:
        sentences = paragraph.split('. ')  # Splitting paragraphs into sentences
        for sentence in sentences:
            quantitative_data = extract_quantitative_data(sentence)
            count = len(quantitative_data)  # Counting the number of quantitative data occurrences in each sentence
            sentence_counts.append(count)
    return sentence_counts

def create_histogram(sentence_counts):
    plt.hist(sentence_counts, bins=max(sentence_counts)+1, edgecolor='black')
    plt.xlabel('Frequency of Quantitative Data')
    plt.ylabel('Number of Sentences')
    plt.title('Distribution of Quantitative Data in Sentences')
    plt.show()
folder_path = 'processed_data'
paragraphs = []
count=0
for filename in os.listdir(folder_path):
    if count >= 1:
        break
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            if 'claim_text' in data:
                paragraphs.append(data['claim_text'])
                count+=1

# Count quantitative data occurrences in each sentence
sentence_counts = count_quantitative_data(paragraphs)
# Create histogram
create_histogram(sentence_counts)
