# Càrrega dels mòduls necessaris per al bon funcionament de l'eina
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

def infer(model, list):
    test_data = word_tokenize(input)
    v1 = model.infer_vector(test_data)
    model.docvecs.most_similar([v1], topn = 7425)[0][0]

def main():
    model = Doc2Vec.load("model.doc2vec")
    # in some way, a dictionary is created with the ips...
    list = ["8.8.8.8", "8.8.4.4"]
    result = infer(model, list)