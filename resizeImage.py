import cv2
import numpy

def load_image(path_img):
    return cv2.imread(path_img)

def bgr2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def main():
    path_img = "images/IMG_2686.jpg"
    img = load_image(path_img)

    # resize to scale 0.2 (di perkecil) soalnya kalo tidak di resize layarnya tidak cukup
    imgResize = cv2.resize(img, None, fx=0.2, fy=0.2)

    # menjadikan image ke bentuk gray
    imgGray = bgr2gray(imgResize)

    # apply guassian blur on src image
    imgBlur = cv2.GaussianBlur(imgResize,(15,15),cv2.BORDER_DEFAULT)

    img_draw = imgResize.copy()

    
    cv2.imshow("Image", imgBlur)


if __name__ == '__main__':
    main()
    cv2.waitKey(0)