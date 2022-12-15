import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    with open(dataPath) as t:
      for i in range(0, 2):
        filename, facenum = t.readline().split()
        # print(filename, facenum)
        img = cv2.imread(os.path.join('data/detect', filename))
        for j in range(0, int(facenum)):
          x, y, xplus, yplus = t.readline().split()
          # print(x, y, xplus, yplus)
          crop_img = img[int(y):int(y)+int(yplus), int(x):int(x)+int(xplus)]
          gray_image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
          final_image = cv2.resize(gray_image, (19, 19))
          result = clf.classify(final_image)
          if result == 1:
            cv2.rectangle(img, (int(x), int(y)), (int(x)+int(xplus), int(y)+int(yplus)), (0, 255, 0), 3)
          else:
            cv2.rectangle(img, (int(x), int(y)), (int(x)+int(xplus), int(y)+int(yplus)), (0, 0, 255), 3)
        cv2.imshow("Detected image", img)
        cv2.waitKey(0)
    # Open detextData.txt and read the file with following format:
    #-------------------------------------------------------------
    # file(image)_name number_of_face
    # faceN_x faceN_y faceN_width faceN_height
    #-------------------------------------------------------------
    # Read and crop the images with the coordinates
    # Convert the image into grayscale and resize the image into 19*19
    # Classify the image with clf.classify()
    # Draw rectangles on the image with green or red color representing whether the face is detected or not
    # Show the results

    # End your code (Part 4)


        
    