# Càrrega dels mòduls necessaris per al bon funcionament de l'eina
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import os
# Aquesta funció serveix per, a partir d'un arxiu .third, obtenir el seu contingut. La variable "zerothird" es refereix a
# d'alternatives desenvolupades i no té utilitat a la sol·lució finalment proposada. Vegeu la secció quatre
# de la memòria del projecte per a més informació
def getInput(file):
    global zerothird
    f = os.open("./third/"+file, os.O_RDONLY)
    aux = os.read(f, os.path.getsize(f))
    aux = str(aux, 'utf-8')
    if os.path.getsize(f) == 0:
        zerothird += 1
    os.close(f)
    return aux
# Inicialització dels comptadors d'encerts i de zerothird
zerothird = 0
oks = 0
# Opertura del model Doc2Vec
model= Doc2Vec.load("model.doc2vec")
# Per a cada arxiu .third que estigui present al directori
for file in os.listdir('./third'):
    input = getInput(file)
    # Prepara les .third per a poder-les inferir amb el model
    test_data = word_tokenize(input)
    # Infereix amb el vector i agafa el document més similar
    v1 = model.infer_vector(test_data)
    similar_doc = model.docvecs.most_similar([v1], topn = 7425)
    # Agafa la pàgina que tingui més probabilitat de ser la correcta
    resultado = similar_doc[0][0]
    # Mostra el nom de la pàgina, seguit d'una coma i "OK" si ha estat un encert o "KO" altrament. En cas que sigui un encert, suma 1 al comptador
    print(file+",", end='')
    if os.path.splitext(file)[0] == similar_doc[0][0]:
        oks = oks + 1
        print("OK")
    else:
        print("KO")
# Mostra els resultats globals de tota l'execució
print("Nombre d'encerts: " + str(oks))
print("Nombre de zerothirds: " + str(zerothird))
print("Percentatge de precisió: " + str(oks/len(os.listdir('./third'))))
print("Percentatge de precisió descomptant zerothirds: " + str(oks / (len(os.listdir('./third')) - zerothird)))