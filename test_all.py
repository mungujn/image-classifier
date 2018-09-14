import functions
import pytest
from flask import json
from service import app
import os
app.testing = True
client = app.test_client()
# skip = pytest.mark.skip(reason='fixing other tests')


def test_postClassificationJob():
    """test add new classification job
    """
    r = client.post('/classification-job', json={
        'classes': ['cat', 'dog', 'car']
    })
    data = json.loads(r.data)
    print(data)
    assert data['complete'] == False


def test_getClassificatioJob():
    """Test get classifcation job
    """
    job_id = 256
    r = client.get(f'/classification-job/{job_id}')
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'


def test_predictImageClass():
    import classifier
    classifier.loadModel()
    prediction = classifier.predictImageClass(
        '', 'test-classification.jpg')

    assert 'Egyptian_cat' in prediction


def test_getFileNames():
    """test getting local filenames
    """
    files = functions.getFileNames('category-1')
    print(files)
    assert len(files) == 4


def test_moveFile():
    """test moving files using a dummy 9 byte file
    """
    result = functions.moveFile('', 'test-move.txt', '', 'test-moved.txt')
    writeBackFile()
    assert result == 9


def writeBackFile():
    """writes back the moved test file to make sure the test works next time
    """
    path = os.path.join('..', 'files', 'test-move.txt')
    with open(path, 'w') as f:
        f.write('123456789')
