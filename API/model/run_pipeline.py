import pandas as pd 
import os  
from API.model.pipeline import thepipeline
from sklearn.model_selection import train_test_split
import pickle
import sqlite3


TRAINING_DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + '/datasets/train.csv'
TESTING_DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + '/datasets/test.csv'
MODEL_PATH = os.path.dirname(os.path.realpath(__file__)) + '/save_model/save.sav'
DATA_BASE_URI = 'sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/db.sqlite'


def _save_model(model):
  pickle.dump(model, open(MODEL_PATH,'wb'))


def read_train():
#  data = pd.read_csv(TRAINING_DATA_FILE)

  data= pd.read_sql_table(table_name = 'titanic_train', con = DATA_BASE_URI)


# Create your connection.
#  cnx = sqlite3.connect(DATA_BASE_URI)

#  data = pd.read_sql_query("SELECT * FROM titanic_train", cnx)

  X_train = data.drop('Survived',axis=1)
  y_train = data['Survived']

  thepipeline.fit(X_train,y_train)
  print(thepipeline.score(X_train,y_train))
  _save_model(thepipeline)


if __name__ == '__main__':
  read_train()