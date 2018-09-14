import functions
import responses
import random
import threading
import contextlib
import classifier
from flask import Flask, request

app = Flask(__name__)

jobs = {}


@app.route('/classification-job', methods=['POST'])
def classificationJob():
    """Handler for the /classification-job POST endpoint \n
    Creates and starts a classification job. \n
    Returns the job data immediately and classification continues in a background thread.
    """
    try:
        if request.is_json:
            json_data = request.get_json()

            job = {}
            job_id = random.randint(100, 200)
            job['id'] = job_id
            job['classes'] = json_data['classes']
            job['complete'] = False
            job['percentage'] = 0
            jobs[f'{job_id}'] = job

            classification_thread = threading.Thread(
                name=f'classification {job_id}', target=startClassificationJob, args=(job,))
            classification_thread.start()

            return responses.respondCreated(job)
        else:
            return responses.respondBadRequest('No categories defined')
    except Exception as error:
        print('Error: ', error)
        return responses.respondInternalServerError(error)


@app.route('/classification-job/<job_id>', methods=['GET'])
def checkClassificationJobStatus(job_id):
    """Handler for checking the status of a classification job \n
    Responds with the data for the specified job
    """
    try:
        try:
            job = jobs[job_id]
            return responses.respondOk(job)
        except KeyError as error:
            print('Jobs:', jobs)
            return responses.respondBadRequest(f'Job {job_id} not found')
    except Exception as error:
        print('Error:', type(error))
        return responses.respondInternalServerError(error)


def startClassificationJob(job):
    """classify images in a folder
    """
    try:
        classes = job['classes']
        files = functions.getFileNames('../files/all')
        number_of_files = len(files)
        job['number_of_files'] = number_of_files
        job['processed'] = 0
        job_id = job['id']
        print(f'Job {job_id}: Classifying {number_of_files} files has started')

        for file in files:
            with timer(job):
                prediction = classifier.predictImageClass('all', f'{file}')
                for image_class in classes:
                    if image_class in prediction:
                        functions.moveFile(
                            'all', f'{file}', f'{image_class}', f'{file}')
        job['complete'] = True
        print(f'Job {job_id}: Classifying {number_of_files} files has completed')
    except Exception as error:
        print('****error-message****')
        job['complete'] = True
        print(f'Job {job_id}: Classifying {number_of_files} files has failed')
        print(error)
        print('****end-of-error-message****')


@contextlib.contextmanager
def timer(job):
    """Context manager to keep track of a jobs status"""
    try:
        yield
    finally:
        job['processed'] += 1
        number_of_files = job['number_of_files']
        processed = job['processed']
        percentage = int((processed/number_of_files)*100)
        job['percentage'] = percentage
        # job_id = job['id']
        # print(f'Job {job_id} is {percentage} percent complete')


if __name__ == '__main__':
    """Run service.
    For test purposes only. When deploying a webserver process and a more scalable 
    model serving set up is better
    """
    print('\n****loading-classification-model****')
    classifier.loadModel()
    print('****classification-model-loaded****')
    app.run(host='127.0.0.1', port=8080, debug=False)
