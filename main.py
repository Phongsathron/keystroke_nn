from flask import Flask, escape, request, jsonify
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
    
    result_from_model = model.predict(filepath)
    posibleKey, bruteforces, spellCorrect, badPassword = utils.spellchecker_and_neighbour(result_from_model)

    bf_filename = filename[:-4]+'.txt'
    bf_path = os.path.abspath('bruteforce/'+secure_filename(bf_filename))
    bf_file = open(bf_filename, "w+")

    for bruteforce in bruteforces:
        bf_file.write(bruteforce)
    bf_file.close()

    return result

@app.route('/download/')
def download():
    pass
