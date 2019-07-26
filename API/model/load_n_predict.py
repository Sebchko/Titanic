import pickle

def make_prediction(path, data):
    picklemodel = pickle.load(open(path, 'rb'))
    y = data['price']
    X = data.drop('price', axis=1)
    result = picklemodel.predict(X)
    score =  picklemodel.score(X,y)
    print(result)
    print(score)