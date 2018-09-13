import functions
import responses
from flask import Flask, request
app = Flask(__name__)

jobs = {}


@app.route('/classification-job', methods=['POST'])
def newClassificationJob():
    try:
        if request.is_json():
            data = request.get_json()
            return responses.respondCreated(data)
        else:
            return responses.respondBadRequest('No categories defined')
    except Exception as error:
        print('Error: ', type(error))
        return responses.respondInternalServerError(error)
