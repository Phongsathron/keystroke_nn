from flask import Flask, escape, request, jsonify, send_file, url_for
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

from model import Model
import utils

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = Model()

@app.route('/')
def hello():
    return f'Hello, It\'s work!'

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    f = request.files['sound']

    filename = utils.randomStringDigits()+'.m4a'
    filepath = os.path.abspath('audio/'+secure_filename(filename))
    f.save(filepath)
    
    result_from_model = model.predict(filepath)
    posibleKey, bruteforces, spellCorrect, badPassword = utils.spellchecker_and_neighbour(result_from_model)

    bf_filename = filename[:-4]+'.txt'
    bf_path = os.path.abspath('bruteforce/'+secure_filename(bf_filename))
    bf_file = open(bf_path, "w+")

    for bruteforce in bruteforces:
        bf_file.write(bruteforce+"\n")
    bf_file.close()

    result = {}
    result["from-model"] = result_from_model
    result["posible-key"] = posibleKey
    result["from-spellcorrection"] = spellCorrect
    result["from-badpassword"] = badPassword
    result["bruteforces-file"] = url_for('download_bruteforce', filename=bf_filename, _external=True)
    return result

@app.route('/download/bruteforce/<path:filename>', methods=['GET'])
def download_bruteforce(filename):
    uploads = os.path.abspath('bruteforce/'+filename)
    return send_file(uploads, attachment_filename=filename, as_attachment=True)
