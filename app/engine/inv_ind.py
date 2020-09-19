# File to create inverted-index

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os, collections, re

Stopwords = set(stopwords.words('english'))
sws = list(Stopwords)
sws.append("doc")
sws.append("docno")
sws.append("document")
Stopwords = set(sws)

def process_files(file_dir):
    file_to_terms = {}
    unique_words = []
    file_content = {}
    for i, file in enumerate(os.listdir(file_dir)):
        pattern = re.compile('[\W_0-9]+')
        content = open(os.path.join(file_dir, file), 'r').read().lower()
        content = pattern.sub(' ',content)
        cont = content.split()
        cont = [w for w in cont if w not in ["doc", "docno", "document"]]
        content = " ".join(cont)
        file_content[i] = content

        words = content.split()
        words = [word for word in words if word not in Stopwords]
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        file_to_terms[i] = words
        unique_words = unique_words + words
    unique_words = list(set(unique_words))
    return file_to_terms, unique_words, file_content

def get_ii(ftt, uw):
    ii = {}
    for i, word in enumerate(uw):
        ii[word] = {"df": 0, "pos": []}
    for i, (key, val) in enumerate(ftt.items()):
        for j, word in enumerate(uw):
            if word in val:
                ii[word]["df"] += 1
                ctr = collections.Counter(val)
                ii[word]["pos"].append({i: ctr[word]})
    return ii

# def get_doc_names(file_dir):
#     doc_names = {}
#     for i, f in enumerate(os.listdir(file_dir)):
#         doc_names[i] = f
#     return doc_names

def get_inv_ind():
    file_to_terms, unique_words, file_content = process_files("./app/engine/data")
    inv_ind = get_ii(file_to_terms, unique_words)
    # print(file_to_terms)
    return inv_ind, file_content
