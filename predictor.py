import pickle
import pandas as pd
import os

TESTING_DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + '/API/model/datasets/test.csv'
TRAINING_DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + '/API/model/datasets/train.csv'

SAVE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/API/model/save_model/save.sav'
#path = os.path.realpath('test.csv')

df = pd.read_csv(TESTING_DATA_FILE)
df_train = pd.read_csv(TRAINING_DATA_FILE)
#df = pd.read_csv(path)
df.to_json(os.path.dirname(os.path.realpath(__file__)) + '/API/model/datasets/jason.json', orient='records')
df_train.to_json(os.path.dirname(os.path.realpath(__file__)) + '/API/model/datasets/jason_train.json', orient='records')

loaded_model = pickle.load(open(SAVE_PATH, 'rb'))
predict = loaded_model.predict(df)
print(predict)