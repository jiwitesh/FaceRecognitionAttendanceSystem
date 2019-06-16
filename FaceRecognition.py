# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 04:55:02 2019

@author: Jiwitesh
"""

import cv2
import os
import numpy as np

def faceDetection(test_img):
    gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_haar_cascade.detectMultiScale(gray_img, scaleFactor=1.2,minNeighbors=5)

    return faces, gray_img
