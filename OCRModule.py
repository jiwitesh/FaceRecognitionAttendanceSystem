# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:27:15 2019

@author: Jiwitesh
"""
#This file has request-response module to get PAN images from user
#and convert to JSON using google VISION API response

import numpy as np
import cv2
from PIL import Image
import requests
import base64
import re
import PIL.ImageOps
import os
import pandas as pd
from scipy.ndimage.interpolation import zoom
import json
from PIL import ImageEnhance
import time
from pdf2image import convert_from_path
import collections
import io

##CALLING OCR API
def detect_image_text(image):
#     url = 'https://vision.googleapis.com/v1/images:annotate?key=xxxxxxxxx2e32e3242dasdfadxxxxxxxxxx'
# provide the key below to access google vision api
  url = 'https://vision.googleapis.com/v1/images:annotate?key='
  res = []
  img_base64 = base64.b64encode(image)
  ig = str(img_base64)
  ik=ig.replace('b\'','')
  headers={'content-type': 'application/json'}
  data ="""{
    "requests": [
      {
        "image": {
                 "content": '"""+ik[:-1]+"""'

                  },

        "features": [
          {
            "type": "DOCUMENT_TEXT_DETECTION"
          }
        ]
      }
    ]
  }"""
  r = requests.post(url, headers=headers,data=data)
  result = json.loads(r.text)
  return(result)


def frequency_ocr1(r):
    try:
        r['responses'][0]['textAnnotations'][1:]
    except:
        return('0')

    word_infos = []
    for i, number in enumerate(r['responses'][0]['textAnnotations']):
        dic = dict()
        rect = r['responses'][0]['textAnnotations'][i]['boundingPoly']['vertices']
        text = r['responses'][0]['textAnnotations'][i]['description']
        pt1 = []
        pt2 = []
        try:
            pt1 = [rect[0]['x'], rect[0]['y']]
            pt2 = [rect[2]['x'], rect[2]['y']]
        except:
             continue
        dic['boundingBox_list'] = pt1 + pt2
        pt1.extend([-pt1[0] + pt2[0], -pt1[1] + pt2[1]])
        #str(round(pt1))
        dic['boundingBox'] = ', '.join(repr(e) for e in pt1)
        dic['text'] = text
        word_infos.append(dic)
    word_info = word_infos[1:len(word_infos)]
    urls = []
    urlls=[]
    box_cordinate_list = []
    ##########extract only text and boundingbox from dict
    for i in range(len(word_info)):
        box_cordinate_list.append(word_info[i]['boundingBox_list'])
        urls.append(word_info[i]['text'])
        urlls.append(word_info[i]['boundingBox'])

    df = pd.DataFrame({'Rows':urls, 'Co-ordinates':urlls})
    df  = pd.concat([df['Rows'],df['Co-ordinates'].str.split(",",expand= True)],axis =1)
    df.columns = ['Rows21','X','Y','Xh','Yk']
    df[['X','Y','Xh','Yk']] = df[['X','Y','Xh','Yk']].apply(pd.to_numeric)
    df['Xh'] = df['X'] + df['Xh']
    df['Yk'] = df['Y'] + df['Yk']
    return(df)

# To be changed according to the images location

#os.chdir(r'C:\Users\Dell\Desktop\Acadgild\project\ocr\Images_and_output\Query_Images')
#path = r'C:\Users\Dell\Desktop\Acadgild\project\ocr\Images_and_output\Query_Images'


def pan_number(df):
  pan = ""
  for i in range(0,len(df)):
    text = df.iloc[i]['Rows21']
    if(re.search("[A-Z]{5}[0-9]{4}[A-Z]",text)):
      pan = text
      return pan
  pan = "not readable"
  return pan

def personName(df):
  personName = ""
  for i in range(0,len(df)):
    text = df.iloc[5]['Rows21']
    if(re.search("[A-Z]",text)):
      personName = text
    text2 = df.iloc[6]['Rows21']
    if (re.search("[A-Z]",text2)):
        personName = personName +" "+text2

    return personName
  personName = "not readable"
  return personName

# to covert tif image to jpg
#from PIL import Image
#im = Image.open(r"C:\Users\Dell\Desktop\Acadgild\project\ocr\Images_and_output\Query_Images\000080.tif")
#im.save(r"C:\Users\Dell\Desktop\Acadgild\project\ocr\Images_and_output\Query_Images\000080.jpg", dpi=(600,600) )


# Below code works well only for single image for which name is given and written considering a PAN card
def readIdText(filename):
    filename = 'img6.jpg'
    new_file_name = filename
    image_bytes = open(new_file_name,'rb')
    image_bytes = image_bytes.read()
    image = np.array(Image.open(io.BytesIO(image_bytes)))
    image_bytes = cv2.imencode('.jpg',image)[1].tostring()
    response = detect_image_text(image_bytes)
    df = frequency_ocr1(response)
    return df

