from sklearn.pipeline import Pipeline
from API.model.preprocessing import Ageimputer , Title_extractor , Some_transformation, Labelizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df = pd.read_csv('/home/sebchko/Desktop/BeCode/pipeline ex/titanic/API/model/datasets/train.csv')
to_label = ['Sex','Cabin','Embarked','Title']


thepipeline=Pipeline(
    [
    ('step1', Ageimputer()),
    ('step2', Title_extractor()),    
    ('step3', Some_transformation()),
    ('step4', Labelizer(to_label)),
    ('modelling', RandomForestClassifier())
])