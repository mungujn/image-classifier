import functions
import pytest
from flask import json
from service import app
app.testing = True
client = app.test_client()
skip = pytest.mark.skip(reason='fixing other tests')



def test_postClassificationJob():
    """test add new classification job
    """
    r = client.post('/classification-job', dict)
    data = json.loads(r.data)
    assert data['complete'] == False


test_postClassificationJob()
