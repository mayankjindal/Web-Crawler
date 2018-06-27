from bs4 import BeautifulSoup
import requests
import nltk
import pickle

tokens = list()
inv_ind = dict()

try:
    f1 = open('tokens.txt', 'r')

    for line in f1:
        tokens.append(line.rstrip())
except:
    f1 = open('tokens.txt', 'a')

try:
    f2 = open('inv_index.pkl', 'rb')
    f2.seek(0)
    inv_ind = pickle.load(f2)
    f2.close()
except:
    pass


class tokenizing:

    def create_tokens(self, url):
        global inv_ind
        global tokens
        ur = requests.get(url)
        be = BeautifulSoup(ur.text, 'lxml')
        for s in be(["script", "style"]):
            s.extract()
        t = list(nltk.word_tokenize(str(be.text)))
        for k in t:
            tokens.append(k)
            if k not in inv_ind.keys():
                inv_ind[k] = []
            if url not in inv_ind[k]:
                inv_ind[k].append(url)

    def save_matrix(self):
        global tokens
        global inv_ind
        f1.close()
        f2 = open('inv_index.pkl', 'bw')
        pickle.dump(inv_ind, f2)
        f = open('tokens.txt', 'r')
        t = set()
        for line in f:
            t.add(line.rstrip())
        # print(inv_ind)
        f.close()
        tokens = set(tokens)
        f = open('tokens.txt', 'a')
        for i in tokens:
            if i not in t:
                f.write(str(i))
                f.write("\n")
        f.close()
        f2.close()
