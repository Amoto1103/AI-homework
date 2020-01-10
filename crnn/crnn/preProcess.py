import numpy as np
import cv2

def preprocess(filein):
    im=cv2.imread(filein,0)
    height,weight=im.shape
    for i in range(height):
        for j in range(weight):
            if i < 1 or i > (height-2) or j < 1 or j >(weight-2):
                im[i,j]=255
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    dilation=cv2.dilate(im,kernel)
    newkernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,2))
    eroded=cv2.erode(dilation,newkernel)
    final=eroded
    cv2.threshold(eroded, 245, 255, cv2.THRESH_BINARY, final)
    cv2.imwrite(filein,final)

