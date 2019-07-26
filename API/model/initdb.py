from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Blueprint, request, jsonify
from ..predictor_API import make_prediction
from .run_pipeline import read_train
from flask_sqlalchemy import SQLAlchemy
from sqlitestuffs import create_connection, delete_all_tasks
import pandas as pd
import sqlite3
import os


def initdb(server, db , ma):

    basedir = os.path.abspath(os.path.dirname(__file__))     
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')

    prediction_app = Blueprint('prediction_route',__name__)

    class TitanicTrain(db.Model):
        PassengerId = db.Column(db.Integer, primary_key=True)
        Survived = db.Column(db.Integer)
        Pclass = db.Column(db.Integer)
        Name = db.Column(db.String, unique=True)
        Sex = db.Column(db.String)
        Age = db.Column(db.Float)
        SibSp = db.Column(db.Integer)
        Parch = db.Column(db.Integer)
        Ticket = db.Column(db.String)
        Fare = db.Column(db.Float)
        Cabin = db.Column(db.String)
        Embarked = db.Column(db.String)
        
        def __init__(self, PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked):
            self.PassengerId = PassengerId
            self.Pclass = Pclass
            self.Survived = Survived
            self.Name = Name
            self.Sex = Sex
            self.Age = Age
            self.SibSp = SibSp 
            self.Parch = Parch
            self.Ticket = Ticket
            self.Fare = Fare
            self.Cabin = Cabin
            self.Embarked = Embarked

    class TitanicTest(db.Model):
        PassengerId = db.Column(db.Integer, primary_key=True)
#        Survived = db.Column(db.Integer)
        Pclass = db.Column(db.Integer)
        Name = db.Column(db.String, unique=True)
        Sex = db.Column(db.String)
        Age = db.Column(db.Float)
        SibSp = db.Column(db.Integer)
        Parch = db.Column(db.Integer)
        Ticket = db.Column(db.String)
        Fare = db.Column(db.Float)
        Cabin = db.Column(db.String)
        Embarked = db.Column(db.String)
        
        def __init__(self, PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked):
            self.PassengerId = PassengerId
            self.Pclass = Pclass
            self.Name = Name
            self.Sex = Sex
            self.Age = Age
            self.SibSp = SibSp 
            self.Parch = Parch
            self.Ticket = Ticket
            self.Fare = Fare
            self.Cabin = Cabin
            self.Embarked = Embarked  

    class TitanicPrediction(db.Model):
        PassengerId = db.Column(db.Integer, primary_key=True)
        Survived = db.Column(db.Integer)
        Pclass = db.Column(db.Integer)
        Name = db.Column(db.String)#, unique=True)
        Sex = db.Column(db.String)
        Age = db.Column(db.Float)
        SibSp = db.Column(db.Integer)
        Parch = db.Column(db.Integer)
        Ticket = db.Column(db.String)
        Fare = db.Column(db.Float)
        Cabin = db.Column(db.String)
        Embarked = db.Column(db.String)
        
        def __init__(self, PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked):
            self.PassengerId = PassengerId
            self.Pclass = Pclass
            self.Name = Name
            self.Sex = Sex
            self.Age = Age
            self.SibSp = SibSp 
            self.Parch = Parch
            self.Ticket = Ticket
            self.Fare = Fare
            self.Cabin = Cabin
            self.Embarked = Embarked               

    class PassengerSchema_train(ma.Schema):
        class Meta:
            fields = ('PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked')

    class PassengerSchema_test(ma.Schema):
        class Meta:
            fields = ('PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked')

    class PassengerSchema_prediction(ma.Schema):
        class Meta:
            fields = ('PassengerId', 'Survived','Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked')                        
         
    db.create_all()
    
    @prediction_app.route('/hello/',methods=['GET'])
    def hello_world():
        return 'Hello, BeCode!'


    @prediction_app.route('/DB_filling', methods=['POST'])
    def db_filling():

        jason = request.json

        for i in range(0,len(jason)):
                        
            PassengerId = jason[i]['PassengerId']
            Survived = jason[i]['Survived']
            Pclass = jason[i]['Pclass']
            Name = jason[i]['Name']
            Sex = jason[i]['Sex']
            Age = jason[i]['Age']
            SibSp = jason[i]['SibSp']
            Parch = jason[i]['Parch']
            Ticket = jason[i]['Ticket']
            Fare = jason[i]['Fare']
            Cabin = jason[i]['Cabin']
            Embarked = jason[i]['Embarked']

            data_base = TitanicTrain(PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked)

            db.session.add(data_base)
            db.session.commit()

        passengers_schema = PassengerSchema_train(many=True, strict=True)
        datas = TitanicTrain.query.all()
        result = passengers_schema.dump(datas)
    
        return jsonify(result.data)

    @prediction_app.route('/DB_test_filling', methods=['POST'])
    def db_filling_test():

        jason = request.json
        goodjob = 'goodjob'
        
        for i in range(0,len(jason)):
                        
            if 'PassengerId' in jason[i]:          
                PassengerId = jason[i]['PassengerId']
            else :                
                goodjob = 'PassengerId is missing'
                break 

            if 'Pclass' in jason[i]:          
                Pclass = jason[i]['Pclass']
            else :
                goodjob = 'Pclass is missing'                
                break            
                
            if 'Name' in jason[i]:          
                Name = jason[i]['Name']
            else :
                goodjob = 'Name is missing'                
                break

            if 'Sex' in jason[i]:          
                Sex = jason[i]['Sex']
            else :
                goodjob = 'Sex is missing'                
                break

            if 'Age' in jason[i]:          
                Age = jason[i]['Age']
            else :
                goodjob = 'Age is missing'                
                break

            if 'SibSp' in jason[i]:          
                SibSp = jason[i]['SibSp']
            else :
                goodjob = 'SibSp is missing'                
                break

            if 'Parch' in jason[i]:          
                Parch = jason[i]['Parch']
            else :
                goodjob = 'Parch is missing'                
                break

            if 'Ticket' in jason[i]:          
                Ticket = jason[i]['Ticket']
            else :
                goodjob = 'Ticket is missing'                
                break

            if 'Fare' in jason[i]:          
                Fare = jason[i]['Fare']
            else :
                goodjob = 'Fare is missing'                
                break

            if 'Cabin' in jason[i]:          
                Cabin = jason[i]['Cabin']
            else :
                goodjob = 'Cabin is missing'                
                break

            if 'Embarked' in jason[i]:          
                Embarked = jason[i]['Embarked']
            else :
                goodjob = 'Embarked is missing'                
                break

            data_base = TitanicTest(PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked)

            db.session.add(data_base)
            db.session.commit()



        #passengers_schema = PassengerSchema_test(many=True, strict=True)
        #datas = TitanicTest.query.all()
        #result = passengers_schema.dump(datas)
    
#        return jsonify(result.data)
        return goodjob        


# get all db
    @prediction_app.route('/DB_train' , methods=['GET'])
    def get_db_train():
        passengers_schema = PassengerSchema_train(many=True, strict=True)
        datas = TitanicTrain.query.all()
        result = passengers_schema.dump(datas)
        return jsonify(result.data)

    # get all db
    @prediction_app.route('/DB_test' , methods=['GET'])
    def get_db_test():
        passengers_schema = PassengerSchema_test(many=True, strict=True)
        datas = TitanicTest.query.all()
        result = passengers_schema.dump(datas)
        return jsonify(result.data)

    @prediction_app.route('/delete_test', methods=['GET'])
    def delete():   
           
    #    DATA_BASE_PATH = str(os.path.dirname(os.path.realpath(__file__)) + '/db.sqlite')
    #    conn = create_connection(DATA_BASE_PATH)
    #    delete_all_tasks(conn)
    # 
        db.session.query(TitanicTest).delete()             
        db.session.commit()

        return('table deleted')    

    @prediction_app.route('/train', methods=['GET'])
    def train():
        read_train()
        return 'Model trained and saved'

    @prediction_app.route('/predict',methods=['POST'])
    def predict():

        jason = request.json 
        goodjob = 'goodjob'       
        
        for i in range(0,len(jason)):
                        
            if 'PassengerId' in jason[i]:          
                PassengerId = jason[i]['PassengerId']
            else :                
                goodjob = 'PassengerId is missing'
                break 

            if 'Pclass' in jason[i]:          
                Pclass = jason[i]['Pclass']
            else :
                goodjob = 'Pclass is missing'                
                break            
                
            if 'Name' in jason[i]:          
                Name = jason[i]['Name']
            else :
                goodjob = 'Name is missing'                
                break

            if 'Sex' in jason[i]:          
                Sex = jason[i]['Sex']
            else :
                goodjob = 'Sex is missing'                
                break

            if 'Age' in jason[i]:          
                Age = jason[i]['Age']
            else :
                goodjob = 'Age is missing'                
                break

            if 'SibSp' in jason[i]:          
                SibSp = jason[i]['SibSp']
            else :
                goodjob = 'SibSp is missing'                
                break

            if 'Parch' in jason[i]:          
                Parch = jason[i]['Parch']
            else :
                goodjob = 'Parch is missing'                
                break

            if 'Ticket' in jason[i]:          
                Ticket = jason[i]['Ticket']
            else :
                goodjob = 'Ticket is missing'                
                break

            if 'Fare' in jason[i]:          
                Fare = jason[i]['Fare']
            else :
                goodjob = 'Fare is missing'                
                break

            if 'Cabin' in jason[i]:          
                Cabin = jason[i]['Cabin']
            else :
                goodjob = 'Cabin is missing'                
                break

            if 'Embarked' in jason[i]:          
                Embarked = jason[i]['Embarked']
            else :
                goodjob = 'Embarked is missing'                
                break

            data_base = TitanicTest(PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked)

            db.session.add(data_base)
            db.session.commit()

        DATA_BASE_URI = 'sqlite:///' + os.path.dirname(os.path.realpath(__file__)) + '/db.sqlite'
        req_data= pd.read_sql_table(table_name = 'titanic_test', con = DATA_BASE_URI)
        db.session.query(TitanicTest).delete()             
        db.session.commit()
        
        prediction = make_prediction(req_data).tolist()
        if goodjob == 'goodjob':
            goodjob = jsonify({'success':True,"prediction": prediction})

        return goodjob

    @prediction_app.route('/health',methods=['GET'])
    def check_health():
        return "Server running"

    return prediction_app 

