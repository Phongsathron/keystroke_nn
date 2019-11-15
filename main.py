from flask import Flask, escape, request
from model import Model

app = Flask(__name__)
model = Model()

@app.route('/')
def hello():
    return f'Hello, It\'s work!'

@app.route('/predict')
def predict():
    model.predict()
