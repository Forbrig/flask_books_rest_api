from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/forbrig/Documentos/projects/flask_books_rest_api/src/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False