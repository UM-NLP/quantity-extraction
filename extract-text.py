from bs4 import BeautifulSoup
import re
import json
from my_dataclass import Patent
import os
import zipfile

zip_file_path = 'C:\\Users\\DELL\\Downloads\\test\\ipa210107.zip'
zip_directory = os.path.dirname(zip_file_path)
xml_file_path = os.path.splitext(zip_file_path)[0] + '.xml'
# Extract the XML file from the ZIP archive
#with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
#    zip_file.extractall(zip_directory)

head="<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
with open(xml_file_path, 'r') as f:
    data = f.read()
pattern = f'(?={re.escape(head)})'
data_splat = re.split(pattern, data)
data_splat=data_splat[1:200]
for xml_data in data_splat:
    Bs_data = BeautifulSoup(xml_data, "xml")
    patent_name=Bs_data.find('country').string+"-"+\
                Bs_data.find('doc-number').string+"-"+\
                Bs_data.find('kind').string
    patent = Patent(patent_name=patent_name)
    claim_text = Bs_data.find_all('claim-text')
    drawing_description=Bs_data.find_all('description-of-drawings')
    abstract=Bs_data.find_all('abstract')
    description=Bs_data.find_all('description')
    patent.claim_text = ''.join([claim_text.get_text() for claim_text in claim_text])
    patent.drawing_description=''.join([drawing_description.get_text() for drawing_description in drawing_description])
    patent.abstract=''.join([abstract.get_text() for abstract in abstract])
    patent.description=''.join([description.get_text() for description in description])
    patent.description = re.sub("\n+", "\n", patent.description)
    patent.abstract = re.sub("\n+", "\n", patent.abstract)
    patent.claim_text = re.sub("\n+", "\n", patent.claim_text)
    patent.drawing_description = re.sub("\n+", "\n", patent.drawing_description)
    patent_json = json.dumps(patent, default=lambda x: x.__dict__, indent=4, ensure_ascii=False)
    with open("data/"+patent_name+".json", 'w', encoding='utf-8') as f:
        f.write(patent_json)