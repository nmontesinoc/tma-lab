from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os

def createTaggedData(dirs):
    tags = list()
    data = list()

    for dir in os.listdir(dirs):
        for file in os.listdir(dirs+dir):
            webpage = os.path.splitext(file)[0]
            tags.append(webpage)
            f = os.open(dirs+dir+'/'+file, os.O_RDONLY)
            aux = os.read(f, os.path.getsize(f))
            aux = str(aux, 'utf-8')
            os.close(f)
            data.append(aux)

    tagged_data = []
    for i in enumerate(data):
        aux = list()
        aux.append(tags[i[0]])
        tagged_data.append(TaggedDocument(words=data[i[0]].split(), tags=aux))
    return tagged_data

def createDoc2Vec():
    model = Doc2Vec(vector_size=200,
                    alpha=0.065,
                    min_alpha=0.00025,
                    min_count=0,
                    dm = 0,
                    window=2,
                    epochs=250,
                    workers=5)
    return model

def trainDoc2Vec(model, tagged_data):
    model.build_vocab(tagged_data)
    model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=250)

def saveDoc2Vec(model):
    model.save("model.doc2vec")

def main():
    tagged_data = createTaggedData('./third/')
    model = createDoc2Vec()
    #tagged_data can be joined as first+second+third+fourth...
    trainDoc2Vec(model, tagged_data)
    saveDoc2Vec(model)

if __name__ == "__main__":
	main()
