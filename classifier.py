from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os
model = None
model_loaded = False


def loadModel():
    global model_loaded
    model_loaded = True
    
    if not model_loaded:
        global model
        model = ResNet50(weights='imagenet')
        


def predictImageClass(folder, image_file_name):
    """Predicts the likely class of an image
    """
    if not model_loaded:
        loadModel()

    path = os.path.join('..', 'files', folder, image_file_name)

    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    predictions = model.predict(x)
    predictions = decode_predictions(predictions, top=1)[0]
    # print('Predicted: ', predictions)
    return predictions[0][1]
