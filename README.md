# Image Classifier Service

[![Build Status](https://travis-ci.com/mungujn/image-classifier.svg?branch=master)](https://travis-ci.com/mungujn/image-classifier)

[![codecov](https://codecov.io/gh/mungujn/image-classifier/branch/master/graph/badge.svg)](https://codecov.io/gh/mungujn/image-classifier)

## Overview

This service classifies the images located in a folder name 'all' into specific classes.
For example, assume the 'all' folder has images of people, cars, trucks and other stuff. The service is then invoked and instructed to classify the images into the classes ['people', 'trucks'].
At the end of the classification job, the working directory will have two extra folders; 'people' and 'trucks' which will contain images of people and trucks respectively.

The service exposes two endpoints;

1. POST '/classification-job'
   This endpoint takes a JSON object with an array of classes that images in the 'all' folder will be classified by.
   It returns a JSON object with data on the started classification jobs, including the job ids.
2. GET '/classification-job/job-id'
   This endpoint is used for checking on the status of a classification job.
   It returns a JSON object that has details on how many images have been classified so far and how many are left.

## Files

1. classifier.py
   Imports keras and tensorflow and then loads the ResNet50 image classification model. The top five predicted classes are concatenated into one string, For example 'car sports_car race_car truck boat'. The string is then checked to see if it has the name of the class being investigated (which is also a string).
2. functions.py
   Contains helper functions for enumerating files in the 'all' folder and for moving a classified image to a different folder.
3. responses.py
   Contains functions for constructing HTTP responses
4. service.py
   The flask app that encapsulates all the functionality of this module and exposes it in the two HTTP endpoints described above.
5. test_all.py
   Contains unit tests for all functions in the classifier.py and functions.py code files. Also contains tests of the two HTTP defined in service.py file.
   To run the tests install pytest then run 'pytest -v'

This service functions independently, but I built it to work in tandem with the downloader/uploader service available [here](https://github.com/mungujn/downloader-uploader). This classifier and the downloader/uploader can be combined and used as a cloud storage image classification system, such as [this](https://github.com/mungujn/image-classification-system).
