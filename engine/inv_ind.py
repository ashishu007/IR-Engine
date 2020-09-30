# File to create inverted-index

# from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os, collections, re, pickle

# Stopwords = set(stopwords.words('english'))
# sws = list(Stopwords)
sws = ["and", "the", "a", "of", "on", "in", "to", "with"]
sws.append("doc")
sws.append("docno")
sws.append("document")
Stopwords = set(sws)

def process_files(file_dir, do_stem, do_stop):
    """
    process the files and create file-to-term dictionary
    """
    # print("inside function")
    file_to_terms = {}
    unique_words = []
    file_content = {}
    total_words = []
    for i, f in enumerate(os.listdir(file_dir)):
        # print("inside for loop")
        pattern = re.compile('[\W_]+')
        content = open(os.path.join(file_dir, f), 'r', encoding="ISO-8859-1").read()
        # content = open(os.path.join(file_dir, file), 'r').read().lower()
        content_line = content.split("\n")
        flag_title_found = False
        abstract = ""
        for ln in content_line:
            if ln != '' and ln[0] != '<':
                # cont = ln.lower()
                # cont = pattern.sub(' ', ln)
                if ln[0] == '#':
                    # abstract = cont
                    abstract = ln[1:]
                elif flag_title_found == False:
                    # title = cont
                    title = ln
                    flag_title_found = True
                elif flag_title_found == True:
                    abstract += ln

        # print("outside for loop")
        # cont = content.split()
        # cont = [w for w in cont if w not in ["doc", "docno", "document"]]
        # content = " ".join(cont)
        # print("(" + f + ")" + title)
        # file_content[i] = {"title": "(" + f + ")" + title, "content": abstract}
        file_content[i] = {"title": title, "content": abstract}

        pattern = re.compile('[\W_0-9]+')
        content = abstract.lower()
        content = pattern.sub(' ',content)
        words = content.split()
        total_words += words
        if do_stop == "yes":
            words = [word for word in words if word not in Stopwords]
        if do_stem =="yes":
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]
        file_to_terms[i] = words
        unique_words = unique_words + words
    unique_words = list(set(unique_words))
    return file_to_terms, unique_words, file_content, list(set(total_words))

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

def get_stats(ii, fc):

    tw = 0
    for k,v in fc.items():
        v_words = v["content"].split()
        tw += len(v_words)

    stats = {
        "Total Documents": len(fc),
        "Total Index Terms from Docs": tw,
        "Number of Posting Lists": len(ii)
    }

    num_postings = 0
    for k, v in ii.items():
        # print(len(v["pos"]))
        num_postings += len(v["pos"])

    stats["Total Number of Postings"] = num_postings

    return stats

def get_inv_ind(corpus, do_stem="yes", do_stop="yes"):
    if os.path.exists("/home/ashishu007/IR-Engine/engine/pkls/inverted_index_{}_stem_{}_stop_removal_{}.pkl".format(corpus, do_stem, do_stop)):
        print("inverted index exists, loading saved one")
        inv_ind = pickle.load(open("/home/ashishu007/IR-Engine/engine/pkls/inverted_index_{}_stem_{}_stop_removal_{}.pkl".format(corpus, do_stem, do_stop), "rb"))
        file_content = pickle.load(open("/home/ashishu007/IR-Engine/engine/pkls/file_content_{}_stem_{}_stop_removal_{}.pkl".format(corpus, do_stem, do_stop), "rb"))

    else:
        print("loading files and creating index ...")
        # print("/home/ashishu007/IR-Engine/engine/data/{}".format(corpus))
        file_to_terms, unique_words, file_content, total_words = process_files("/home/ashishu007/IR-Engine/engine/data/{}".format(corpus), do_stem, do_stop)
        print("files loaded, index created, now creating inverted index ...")
        inv_ind = get_ii(file_to_terms, unique_words)

        pickle.dump(inv_ind, open("/home/ashishu007/IR-Engine/engine/pkls/inverted_index_{}_stem_{}_stop_removal_{}.pkl".format(corpus, do_stem, do_stop), "wb"))
        pickle.dump(file_content, open("/home/ashishu007/IR-Engine/engine/pkls/file_content_{}_stem_{}_stop_removal_{}.pkl".format(corpus, do_stem, do_stop), "wb"))
        # pickle.dump(inv_ind, open("./engine/pkls/inverted_index.pkl", "wb"))
        # pickle.dump(file_content, open("./engine/pkls/file_content.pkl", "wb"))

    # calculate stats
    stats = get_stats(inv_ind, file_content)
    print("inverted ondex created ...")
    print(corpus, do_stem)

    return inv_ind, file_content, stats