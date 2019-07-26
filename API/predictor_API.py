import pickle
import pandas as pd
import os

TESTING_DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + '/model/datasets/test.csv'
SAVE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/model/save_model/save.sav'
#path = os.path.realpath('test.csv')

def make_prediction(input_data):
  if type(input_data) is dict:
    data = pd.DataFrame(input_data, index=[0])
  else :
    data = pd.DataFrame(input_data)

 
  model = pickle.load(open(SAVE_PATH,'rb'))
  return model.predict(data)



