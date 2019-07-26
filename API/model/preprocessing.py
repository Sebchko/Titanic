import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder



### imputing missing age in df ###

class Ageimputer(BaseEstimator, TransformerMixin):
  def __init__(self):
    pass

  def fit(self,X,y):
    return self

  def transform(self,X):
    X = X.copy()
    means = X.groupby('Pclass').Age.median()
    for i in X[X.Age.isnull()].index:
      X.loc[i, 'Age'] = means[X.loc[i].Pclass]
    print('Age Imputer completed')   
    return X


### Title_extractor ###

class Title_extractor (BaseEstimator, TransformerMixin):
  # def __init__(self,df):
  #   self.df = df

  def fit(self,X,y):
    return self

  def transform(self,X):
    df_title = X['Name']
    data_title = [i.split(",")[1].split(".")[0].strip() for i in df_title]
    X["Title"] = pd.Series(data_title)
    X['Title'].replace({'Mme':'Mrs',
                        'the Countess':'Lady',
                        'Mlle':'Miss',
                        'Ms':'Mrs',
                        'Jonkheer':'Sir',
                        'Major':'Col',
                        'Capt':'Col',
                        'Don':'Sir',
                        'Dona':'Lady',
                        }, inplace=True)
    print('Title extractor completed')                
    return X

class Some_transformation(BaseEstimator, TransformerMixin):
  def __init__(self):
    pass
  def fit(self,X,y):
    return self
  def transform(self,X): 
    X = X.copy() 
    X.drop(['Name','Ticket', 'PassengerId'], axis=1, inplace=True)
    X['Fare'] = X['Fare'].fillna(0)
    X["Cabin"] = pd.Series([i[0] if not pd.isnull(i) else 'Unknown' for i in X['Cabin']])
    print('Some_transformation completed')
    return X

class Labelizer(BaseEstimator, TransformerMixin):
  def __init__(self,features):
    self.features = features 
  def fit(self,X,y):

    return self

  def transform(self,X):
    le = LabelEncoder()
    for i in self.features:
      X[i] = X[i].astype(str)
      X[i] = le.fit_transform(X.iloc[:,X.columns.get_loc(i)])
    print('Labelizer complete')
    return X
    

