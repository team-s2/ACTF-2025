# yolov?_cls

An easy adversarial attack challenge, you need to input image into yolo-cls model, and two yolo-cls model will classify your image as two different classes.

The most difficult part of this challenge is to debug the program and find out how yolo preprocess the image before deep learning.

You can just add the preprocessing steps in your attack code, define loss as the sum of CrossEntropyLoss of two models, and attack it using FGSM or other algorithm.

Detail code is in solve.ipynb, and if you have better solution and better result (e.g. max_diff <= 1), please tell me.