from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow as tf
import numpy as np
import os
import common.logger as log
model = None
model_loaded = False
working_dir = 'files'


def loadModel():
    global model_loaded

    if not model_loaded:
        global model
        model = ResNet50(weights='imagenet')
        global graph
        # this will allow the model to be called from a different thread than the defining thread
        graph = tf.get_default_graph()
        model_loaded = True


def predictImageClass(folder, image_file_name):
    '''Returns a string with the top five most likely classes of an image
    '''
    global model
    path = os.path.join(working_dir, folder, image_file_name)

    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # allow the model to be called from a different thread than the defining thread
    with graph.as_default():
        predictions = model.predict(x)

    predictions = decode_predictions(predictions, top=5)[0]

    top_five = ''
    for prediction in predictions:
        top_five += f' {prediction[1]}'
    return top_five
