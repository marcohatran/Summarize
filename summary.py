import json, sys, requests
# import tensorflow as tf
# from keras.models import Sequential
from PIL import Image
import pytesseract
import argparse
import os
import cv2

def processImage(imgUri, preprocess):
    image = cv2.imread(imgUri)
    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == 'thresh':
        greyscale = cv2.threshold(greyscale, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif preprocess == 'blur':
        greyscale = cv2.medianBlur(greyscale, 3)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, greyscale)

    text = pytesseract.image_to_string(Image.open(filename))
    print filename
    os.remove(filename)
    print(text)
    summarize(text)

    # For testing purposes
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Greyscale', greyscale)
    # cv2.waitKey(0)

def summarize(input):
    input_data= {'sm_api_input': input}

    mask = open('mask.json')
    key = json.load(mask)

    request = requests.post("http://api.smmry.com/&SM_API_KEY=" + key['value'], data=input_data).json()
    print request.get('sm_api_content')

def summarizeWebsite(url):
    request = requests.get(url).json()
    print request.get('sm_api_content')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=False, help='path to input image to be read via OCR')
    ap.add_argument('-t', '--text', required=False, help='path of text input to be read')
    ap.add_argument('-u', '--url', required=False, help='url of web page to be read')
    ap.add_argument('-p', '--preprocess', type=str, default='thresh', help='type of preprocessing')
    args = vars(ap.parse_args())

    if args['text'] != None:
        summarize(open(args['text'], 'r').read())
    elif args['url'] != None:
        summarizeWebsite(args['url'])
    else:
        processImage(args['image'], args['preprocess'])
