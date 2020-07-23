import sys
from PIL import Image 
from PIL import ImageFilter
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

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


img = Image.open("jVeUTO.jpg")
img = prepare_image(img)
img = remove_noise(img, 70)
img.save("sample_output.png")