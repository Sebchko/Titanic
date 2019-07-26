from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from API.model.initdb import initdb


def create_app():
  server = Flask('who is going to drawn?')  
  server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  #----------
  db = SQLAlchemy(server)
  ma = Marshmallow(server)
      
  prediction_app = initdb(server, db , ma)
  #----------
  server.register_blueprint(prediction_app)
  return server

