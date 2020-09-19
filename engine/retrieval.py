import pickle
from engine.inv_ind import get_inv_ind

def get_retrieved_docs(q):
    query = q.split()
    connecting_words = []
    different_words = []
    for word in query:
        if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
            different_words.append(word.lower())
        else:
            connecting_words.append(word.lower())
    # print("connecting_words", connecting_words)
    # print("different_words", different_words)

    # inv_ind, file_content = get_inv_ind()
    inv_ind = pickle.load(open("./engine/pkls/inverted_index.pkl", "rb"))
    file_content = pickle.load(open("./engine/pkls/file_content.pkl", "rb"))

    total_files = len(list(file_content.keys()))

    unique_words_all = list(inv_ind.keys())

    zeroes_and_ones = []
    zeroes_and_ones_of_all_words = []
    flag_not_found = True # flag for checking if word doesnt exist
    for word in (different_words):
        # print(word)
        if word.lower() in unique_words_all:
            flag_not_found = False
            zeroes_and_ones = [0] * total_files
            # print(inv_ind[word.lower()]["pos"])
            locs = [k for d in inv_ind[word.lower()]["pos"] for k, v in d.items()]
            # print(locs)
            for i in locs:
                zeroes_and_ones[i] = 1
            zeroes_and_ones_of_all_words.append(zeroes_and_ones)
        # else:
        #     print("word not found")
        #     flag = True
    # print(zeroes_and_ones_of_all_words)

    # flag_no_match = True # flag to check if no match is found for documents

    # if len(zeroes_and_ones_of_all_words) > 1:
    #     flag_no_match = False
    # print("flag_no_match", flag_no_match)
    # print("flag_not_found and flag_no_match", flag_not_found and flag_no_match)
    if not flag_not_found:
        for word in connecting_words:
            try:
                word_list1 = zeroes_and_ones_of_all_words[0]
                word_list2 = zeroes_and_ones_of_all_words[1]
                # print("word_list1, word_list2", word_list1, word_list2)
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
                    bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,bitwise_op)]
            except:
                flag_not_found = True
        retrieved_docs = []
        lis = zeroes_and_ones_of_all_words[0]
        # print(lis)
        flag_no_match = True
        for i, index in enumerate(lis):
            if index == 1:
                flag_no_match = False
                # print(i, index)
                retrieved_docs.append({i: file_content[i]})
        # print(files)
    # if flag_no_match:
    #     retrieved_docs = [{"null": "no match found"}]
    if flag_not_found:
        retrieved_docs = [{"null": "not found"}]

    return retrieved_docs