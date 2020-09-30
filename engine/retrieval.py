import pickle
from engine.inv_ind import get_inv_ind

def get_retrieved_docs(q, c, s, sw):
    query = q.split()
    connecting_words = []
    different_words = []
    for word in query:
        if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
            different_words.append(word.lower())
        else:
            connecting_words.append(word.lower())

    if len(connecting_words) == 0:
        for i in range(len(different_words)-1):
            connecting_words.append("or")

    print("connecting_words", connecting_words)
    print("different_words", different_words)
    
    inv_ind = pickle.load(open("./engine/pkls/inverted_index_{}_stem_{}_stop_removal_{}.pkl".format(c, s, sw), "rb"))
    file_content = pickle.load(open("./engine/pkls/file_content_{}_stem_{}_stop_removal_{}.pkl".format(c, s, sw), "rb"))
    
    total_files = len(list(file_content.keys()))
    unique_words_all = list(inv_ind.keys())

    zeroes_and_ones = []
    zeroes_and_ones_of_all_words = []
    flag_not_found = True # flag for checking if word doesnt exist
    for word in (different_words):
        if word.lower() in unique_words_all:
            flag_not_found = False
            zeroes_and_ones = [0] * total_files
            locs = [k for d in inv_ind[word.lower()]["pos"] for k, v in d.items()]
            for i in locs:
                zeroes_and_ones[i] = 1
        else:
            zeroes_and_ones = [0] * total_files
        zeroes_and_ones_of_all_words.append(zeroes_and_ones)

    print(zeroes_and_ones_of_all_words)

    if not flag_not_found:
        for word in connecting_words:
            try:
                word_list1 = zeroes_and_ones_of_all_words[0]
                word_list2 = zeroes_and_ones_of_all_words[1]
                if word == "and":
                    bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,word_list2)]
                    zeroes_and_ones_of_all_words.remove(word_list1)
                    zeroes_and_ones_of_all_words.remove(word_list2)
                    zeroes_and_ones_of_all_words.insert(0, bitwise_op)
                elif word == "or":
                    bitwise_op = [w1 | w2 for (w1,w2) in zip(word_list1,word_list2)]
                    zeroes_and_ones_of_all_words.remove(word_list1)
                    zeroes_and_ones_of_all_words.remove(word_list2)
                    zeroes_and_ones_of_all_words.insert(0, bitwise_op)
                elif word == "not":
                    bitwise_op = [not w1 for w1 in word_list2]
                    bitwise_op = [int(b == True) for b in bitwise_op]
                    zeroes_and_ones_of_all_words.remove(word_list2)
                    zeroes_and_ones_of_all_words.remove(word_list1)
                    print(word_list1, word_list2, bitwise_op)
                    bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,bitwise_op)]
                    zeroes_and_ones_of_all_words.insert(0, bitwise_op)
            except:
                flag_not_found = True
        retrieved_docs = []
        print(zeroes_and_ones_of_all_words)
        try:
            lis = zeroes_and_ones_of_all_words[0]
            flag_no_match = True
            for i, index in enumerate(lis):
                if index == 1:
                    flag_no_match = False
                    retrieved_docs.append({i: file_content[i]})
            if flag_no_match == True:
                flag_not_found = True
        except:
            flag_not_found = True

    if flag_not_found:
        retrieved_docs = [{"null": "not found"}]

    return retrieved_docs