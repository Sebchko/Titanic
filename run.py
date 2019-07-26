import sys
sys.path.append('API/model')
from API.app import create_app

#server, Titanic, db, passengers_schema = create_app()
server = create_app()

server.run(debug=True)