import cv2
import numpy

def load_image(path_img):
    return cv2.imread(path_img)

def bgr2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def bgr2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def main():
    path_img = "images/IMG_2686.jpg"
    img = load_image(path_img)

    #$input
    size = string(input('Please enter resize 0.?: '))

    # resize to scale 0.2 (di perkecil) soalnya kalo tidak di resize layarnya tidak cukup
    imgResize = cv2.resize(img, None, fx=size, fy=size)

    # menjadikan image ke bentuk gray
    imgGray = bgr2gray(imgResize)

    # menjadikan image ke bentuk hsv
    imgHsv = bgr2hsv(imgResize)

    #img_draw = imgResize.copy()

    #Menampilan gambar di window
    cv2.imshow("Image", imgHsv)


if __name__ == '__main__':
    main()
    cv2.waitKey(0)