# File to create inverted-index

# from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os, collections, re, pickle

# Stopwords = set(stopwords.words('english'))
# sws = list(Stopwords)
sws = ["a", "an", "the", "they", "i", "am", "you", "with", "on", "to", "was"]
sws.append("doc")
sws.append("docno")
sws.append("document")
Stopwords = set(sws)

def process_files(file_dir):
    """
    process the files and create file-to-term dictionary
    """
    file_to_terms = {}
    unique_words = []
    file_content = {}
    for i, file in enumerate(os.listdir(file_dir)):
        pattern = re.compile('[\W_]+')
        content = open(os.path.join(file_dir, file), 'r').read()
        # content = open(os.path.join(file_dir, file), 'r').read().lower()
        content_line = content.split("\n")
        for ln in content_line:
            if ln != '' and ln[0] != '<':
                # cont = ln.lower()
                cont = pattern.sub(' ', ln)
                if ln[0] == '#':
                    abstract = cont
                else:
                    title = cont

        # cont = content.split()
        # cont = [w for w in cont if w not in ["doc", "docno", "document"]]
        # content = " ".join(cont)
        file_content[i] = {"title": title, "content": abstract}

        pattern = re.compile('[\W_0-9]+')
        content = content.lower()
        content = pattern.sub(' ',content)
        words = content.split()
        words = [word for word in words if word not in Stopwords]
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        file_to_terms[i] = words
        unique_words = unique_words + words
    unique_words = list(set(unique_words))
    return file_to_terms, unique_words, file_content

def get_ii(ftt, uw):
    """
    get the inverted index
    """
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

def get_inv_ind(load_saved=True):
    # if not os.path.exists("./app/engine/pkls/inverted_index.pkl"):
    #     load_saved = False
    # if not load_saved:
    print("loading files and creating index ...")
    file_to_terms, unique_words, file_content = process_files("./engine/data")
    print("files loaded, index created, now creating inverted index ...")
    inv_ind = get_ii(file_to_terms, unique_words)
    print("inverted ondex created ...")
    pickle.dump(inv_ind, open("./engine/pkls/inverted_index.pkl", "wb"))
    pickle.dump(file_content, open("./engine/pkls/file_content.pkl", "wb"))
    # else:
    #     print("loading saved inverted_index")
    #     inv_ind = pickle.load(open("./app/engine/pkls/inverted_index.pkl", "rb"))
    #     file_content = pickle.load(open("./app/engine/pkls/file_content.pkl", "rb"))
    return inv_ind, file_content
