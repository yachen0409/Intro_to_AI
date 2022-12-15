import os
import cv2
import numpy as np

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    dataset = []
    realpath = os.path.join(dataPath, 'face')
    for filename in os.listdir(realpath):
      data = cv2.imread(os.path.join(realpath, filename), cv2.IMREAD_GRAYSCALE)
      datatuple = (data, 1)
      dataset.append(datatuple)
    realpath = os.path.join(dataPath, 'non-face')
    for filename in os.listdir(realpath):
      data = cv2.imread(os.path.join(realpath, filename), cv2.IMREAD_GRAYSCALE)
      datatuple = (data, 0)
      dataset.append(datatuple)
    # Read the pgm file inside face and non-face folder in grayscale mode with cv2.imread()
    # Append classification (face = 1, non-face = 0)
    # Append (data, classification) tuple on dataset and return
    
    # End your code (Part 1)
    return dataset
