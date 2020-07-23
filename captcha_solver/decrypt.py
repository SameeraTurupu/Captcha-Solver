import sys
from PIL import Image 
from PIL import ImageFilter
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import os

def prepare_image(img):
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    if 'L' != img.mode:
        img = img.convert('L')
    return img

def remove_noise(img, pass_factor):
    for column in range(img.size[0]):
        for line in range(img.size[1]):
            value = remove_noise_by_pixel(img, column, line, pass_factor)
            img.putpixel((column, line), value)
    return img

def remove_noise_by_pixel(img, column, line, pass_factor):
    if img.getpixel((column, line)) < pass_factor:
        return (0)
    return (255)



directory = r'/Users/sameeraturupu/Desktop/captchas'
path, dirs, files = next(os.walk(directory))
correct = 0
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        filename = (os.path.join(directory, filename))
        img = Image.open(filename)
        img = prepare_image(img)
        img = remove_noise(img, 51)
        img.save("sample_output.png")
        img = Image.open('sample_output.png').convert('L')
        ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)

        img = Image.fromarray(img.astype(np.uint8))
        res = ''.join(re.findall("[a-zA-Z0-9]", pytesseract.image_to_string(img, lang='eng', \
                config='tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')))
        filename = str(filename[filename.rfind("/") + 1:filename.find(".")])
        if(res == filename):
            correct += 1
            print("Matched: ", res)
        else:
            print(filename + " != " + res)
    else:
        continue

print("accuracy " + str((correct/len(files)) * 100))
    
