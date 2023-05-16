# from quantulum3 import parser
# text="The resulting BaCO3 had a crystallite size of between about 20 and 40 nm."
# quants = parser.parse(text)
# print(quants)
import yaml
def sentence_detection(text):
    doc = nlp(text)
    sentences = []
    for i in range (0, len (doc.sents)):
        if len(doc.sents[i])>100:
            sentences.append(doc.sents[i])
        else:
            sentences.append(doc.sents[i]+" "+doc.sents[i+1])
            i=i+1
    return sentence
