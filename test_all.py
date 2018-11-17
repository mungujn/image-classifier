import os
import functions
import pytest
from flask import Flask, json
from service import app
app.testing = True
client = app.test_client()
# skip = pytest.mark.skip(reason='fixing other tests')


def test_postClassificationJob():
    '''test add new classification job
    '''
    r = client.post('/classification-job', json={
        'classes': ['cat', 'dog', 'car']
    }, headers={'Authorization': os.environ['SERVICE_KEY']})
    data = json.loads(r.data)
    print(data)
    assert data['complete'] == False


# test_postClassificationJob()


def test_getClassificatioJob():
    '''Test get classifcation job
    '''
    job_id = 256
    r = client.get(
        f'/classification-job/{job_id}', headers={'Authorization': os.environ['SERVICE_KEY']})
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'

# test_getClassificatioJob()


def test_predictImageClass():
    import classifier
    classifier.loadModel()
    prediction = classifier.predictImageClass(
        '', 'test-classification.jpg')

    assert 'Egyptian_cat' in prediction

# test_predictImageClass()


def test_getFileNames():
    '''test getting local filenames
    '''
    files = functions.getFileNames('category-1')
    print(files)
    assert len(files) == 4

# test_getFileNames()


def test_moveFile():
    '''test moving files using a dummy 9 byte file
    '''
    result = functions.moveFile('', 'test-move.txt', '', 'test-moved.txt')
    writeBackFile()
    assert result == 9


def writeBackFile():
    '''writes back the moved test file to make sure the test works next time
    '''
    path = os.path.join('files', 'test-move.txt')
    with open(path, 'w') as f:
        f.write('123456789')


# test_moveFile()


def test_common():
    '''test general files to improve coverage
    Simply run to make sure they dont crash the application
    '''
    from common import logger, responses
    logger.obj('string')

    app = Flask(__name__)

    with app.app_context():
        responses.respondInternalServerError()
        responses.respondOk('string')
        responses.respondUnauthorized('string')
        responses.respondWithData({'key': 'value'})


test_common()
