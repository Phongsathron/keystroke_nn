from flask import Flask, escape, request
from werkzeug.utils import secure_filename
import os

from model import Model
import utils

app = Flask(__name__)
model = Model()

@app.route('/')
def hello():
    return f'Hello, It\'s work!'

@app.route('/predict', methods=['POST'])
def predict():
    f = request.files['sound']

    filename = utils.randomStringDigits()+'.m4a'
    filepath = os.path.abspath('audio/'+secure_filename(filename))
    f.save(filepath)
    
    result = model.predict(filepath)
    return result
