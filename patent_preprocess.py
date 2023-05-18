from bs4 import BeautifulSoup
import re
import json
import os
import zipfile
HAED = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

def load_files(zip_file_path): #unzip the zip file and split the xml to seperate patents
    zip_directory = os.path.dirname(zip_file_path)
    xml_file_path = os.path.splitext(zip_file_path)[0] + '.xml'
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file: # Extract the XML file from the ZIP archive
        zip_file.extractall(zip_directory)
    with open(xml_file_path, 'r') as f:
        data = f.read()
    pattern = f'(?={re.escape(HAED)})'
    splat_xml = re.split(pattern, data)
    splat_xml = splat_xml[1:200]
    return splat_xml

def preprocess(data_splat):
    for xml_data in data_splat:
        Bs_data = BeautifulSoup(xml_data,  features="html.parser") #can also try lxml feature
        patent_name = Bs_data.find('country').string+"-"+\
                    Bs_data.find('doc-number').string+"-"+\
                    Bs_data.find('kind').string

        claim_text = Bs_data.find_all('claim-text')
        drawing_description = Bs_data.find_all('description-of-drawings')
        abstract = Bs_data.find_all('abstract')
        description = Bs_data.find_all('description')
        claim_text = ''.join([claim_text.get_text() for claim_text in claim_text]) # concat paragraphs
        drawing_description = ''.join([drawing_description.get_text() for drawing_description in drawing_description]) # concat paragraphs
        abstract = ''.join([abstract.get_text() for abstract in abstract]) # concat paragraphs
        description = ''.join([description.get_text() for description in description]) # concat paragraphs
        description = re.sub("\n+", "\n", description) # remove extra new lines
        abstract = re.sub("\n+", "\n", abstract) # remove extra new lines
        claim_text = re.sub("\n+", "\n", claim_text) # remove extra new lines
        drawing_description = re.sub("\n+", "\n", drawing_description) # remove extra new lines
        result = {"patent_name": patent_name, "claim_text":claim_text, "drawing_description": drawing_description, "description":description, "abstract": abstract}
        patent_json = json.dumps(result, indent=4, ensure_ascii=False)
        with open("processed_data/"+patent_name+".json", 'w', encoding='utf-8') as f:
            f.write(patent_json)

zip_file = 'processed_data/ipa210121.zip'
splat_xml = load_files(zip_file)
preprocess(splat_xml)