import cv2
import numpy as np


def load_image(path_img):
    return cv2.imread(path_img)


def bgr2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def setRangeColor(hsv, lower_color, upper_color):
    return cv2.inRange(hsv, lower_color, upper_color)


def contours_img(mask):
    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filter_contours_img(contours, img_draw, color_bbox):
    count = 0
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        area = w * h

        if area > 1000:
            count = count + 1
            cv2.rectangle(img_draw, (x, y), (x+w, y+h), color_bbox, 5)
    return img_draw, count


def draw_text_on_image(img_draw, count_yellow, count_orange, count_blue):
    #cv2.rectangle(img_draw, (0, 0), (500, 120), (0, 0, 0), -1)
    cv2.putText(img_draw, 'Red Count : ' + str(count_orange),
                (10, 50),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                0.5,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType

    cv2.putText(img_draw, 'Green Count : ' + str(count_yellow),
                (10, 100),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                0.5,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType
    cv2.putText(img_draw, 'Yellow Count : ' + str(count_blue),
                (10, 150),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                0.5,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType
    count_total = count_yellow+count_orange+count_blue
    cv2.putText(img_draw, 'Total Count : ' + str(count_total),
                (10, 200),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                0.5,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType
    return img_draw


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def empty(a):
    pass


def main():
    # include image
    path_img = "images/IMG_2686.jpg"
    img = load_image(path_img)
    # print(img.shape)

    # resize to scale 0.2 (di perkecil)
    imgResize = cv2.resize(img, None, fx=0.2, fy=0.2)
    # print(imgResize.shape)

    # menjadikan image ke bentuk hsv
    imgHsv = bgr2hsv(imgResize)

    img_draw = imgResize.copy()

    # Trackbar Yellow
    cv2.namedWindow("TrackBars1")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars1", 20, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars1", 45, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars1", 100, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars1", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars1", 100, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars1", 255, 255, empty)

    # Trackbar Orange
    cv2.namedWindow("TrackBars2")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars2", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars2", 20, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars2", 150, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars2", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars2", 150, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars2", 255, 255, empty)

    while True:
        # setting yellow
        h_min1 = cv2.getTrackbarPos("Hue Min", "TrackBars1")
        h_max1 = cv2.getTrackbarPos("Hue Max", "TrackBars1")
        s_min1 = cv2.getTrackbarPos("Sat Min", "TrackBars1")
        s_max1 = cv2.getTrackbarPos("Sat Max", "TrackBars1")
        v_min1 = cv2.getTrackbarPos("Val Min", "TrackBars1")
        v_max1 = cv2.getTrackbarPos("Val Max", "TrackBars1")
        print("Yellow : ", h_min1, h_max1, s_min1, s_max1, v_min1, v_max1)

        # setting orange
        h_min2 = cv2.getTrackbarPos("Hue Min", "TrackBars2")
        h_max2 = cv2.getTrackbarPos("Hue Max", "TrackBars2")
        s_min2 = cv2.getTrackbarPos("Sat Min", "TrackBars2")
        s_max2 = cv2.getTrackbarPos("Sat Max", "TrackBars2")
        v_min2 = cv2.getTrackbarPos("Val Min", "TrackBars2")
        v_max2 = cv2.getTrackbarPos("Val Max", "TrackBars2")
        print("Orange : ", h_min2, h_max2, s_min2, s_max2, v_min2, v_max2)

        # medefinisikan kuning di HSV
        lower_Yellow = np.array([h_min1, s_min1, v_min1])  # 20 100 100
        upper_Yellow = np.array([h_max1, s_max1, v_max1])  # 45 255 255
        mask_Yellow = setRangeColor(imgHsv, lower_Yellow, upper_Yellow)
        contours = contours_img(mask_Yellow)
        color_bbox = (0, 0, 255)  # warna shape detection
        img_draw, count_yellow = filter_contours_img(
            contours, img_draw, color_bbox)
        print('Yellow Count:', count_yellow)
        result_Yellow = cv2.bitwise_and(imgResize, imgResize, mask=mask_Yellow)

        # define range of Orange color in HSV
        lower_Orange = np.array([h_min2, s_min2, v_min2])  # 0 150 150
        upper_Orange = np.array([h_max2, s_max2, v_max2])  # 20 255 255
        mask_Orange = setRangeColor(imgHsv, lower_Orange, upper_Orange)
        contours = contours_img(mask_Orange)
        color_bbox = (0, 255, 0)  # warna shape detection
        img_draw, count_orange = filter_contours_img(
            contours, img_draw, color_bbox)
        print('Orange Count:', count_orange)
        result_Orange = cv2.bitwise_and(imgResize, imgResize, mask=mask_Orange)

        # memberi text dan count pada window
        img_draw = draw_text_on_image(img_draw, count_yellow, count_orange)

        # show image
        # cv2.imshow("Image", img)
        # cv2.imshow("ImageResize", imgResize)
        # cv2.imshow("ImageHsv", imgHsv)
        # cv2.imshow("Range Yellow", mask_Yellow)
        # cv2.imshow("Range Orange", mask_Orange)
        # cv2.imshow("Result Yellow", result_Yellow)
        cv2.imshow("Draw Image", img_draw)

        # image Stack
        imgBlank = np.zeros_like(imgResize)
        imageStack = stackImages(0.4, ([imgResize, imgHsv],
                                       [mask_Yellow, result_Yellow],
                                       [mask_Orange, result_Orange]))
        cv2.imshow("Image Stack", imageStack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main2():
    # video capture
    cap = cv2.VideoCapture(2)

    # Trackbar Red
    cv2.namedWindow("TrackBars1")
    cv2.resizeWindow("TrackBars1", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars1", 132, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars1", 179, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars1", 100, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars1", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars1", 100, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars1", 255, 255, empty)

    # Trackbar Green
    cv2.namedWindow("TrackBars2")
    cv2.resizeWindow("TrackBars2", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars2", 56, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars2", 83, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars2", 97, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars2", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars2", 60, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars2", 255, 255, empty)

    # Trackbar Blue
    cv2.namedWindow("TrackBars3")
    cv2.resizeWindow("TrackBars3", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars3", 10, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars3", 57, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars3", 142, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars3", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars3", 202, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars3", 255, 255, empty)

    while True:
        success, img = cap.read()
        #cv2.imshow("Video", img)

        # menjadikan image ke bentuk hsv
        imgHsv = bgr2hsv(img)

        img_draw = img.copy()

        # setting red
        h_min1 = cv2.getTrackbarPos("Hue Min", "TrackBars1")
        h_max1 = cv2.getTrackbarPos("Hue Max", "TrackBars1")
        s_min1 = cv2.getTrackbarPos("Sat Min", "TrackBars1")
        s_max1 = cv2.getTrackbarPos("Sat Max", "TrackBars1")
        v_min1 = cv2.getTrackbarPos("Val Min", "TrackBars1")
        v_max1 = cv2.getTrackbarPos("Val Max", "TrackBars1")
        print("Red : ", h_min1, h_max1, s_min1, s_max1, v_min1, v_max1)

        # setting green
        h_min2 = cv2.getTrackbarPos("Hue Min", "TrackBars2")
        h_max2 = cv2.getTrackbarPos("Hue Max", "TrackBars2")
        s_min2 = cv2.getTrackbarPos("Sat Min", "TrackBars2")
        s_max2 = cv2.getTrackbarPos("Sat Max", "TrackBars2")
        v_min2 = cv2.getTrackbarPos("Val Min", "TrackBars2")
        v_max2 = cv2.getTrackbarPos("Val Max", "TrackBars2")
        print("Green : ", h_min2, h_max2, s_min2, s_max2, v_min2, v_max2)

        # setting blue
        h_min3 = cv2.getTrackbarPos("Hue Min", "TrackBars3")
        h_max3 = cv2.getTrackbarPos("Hue Max", "TrackBars3")
        s_min3 = cv2.getTrackbarPos("Sat Min", "TrackBars3")
        s_max3 = cv2.getTrackbarPos("Sat Max", "TrackBars3")
        v_min3 = cv2.getTrackbarPos("Val Min", "TrackBars3")
        v_max3 = cv2.getTrackbarPos("Val Max", "TrackBars3")
        print("Blue : ", h_min3, h_max3, s_min3, s_max3, v_min3, v_max3)

        # medefinisikan merah di HSV
        lower_Yellow = np.array([h_min1, s_min1, v_min1])  # 0 100 100
        upper_Yellow = np.array([h_max1, s_max1, v_max1])  # 20 255 255
        mask_Yellow = setRangeColor(imgHsv, lower_Yellow, upper_Yellow)
        contours = contours_img(mask_Yellow)
        color_bbox = (0, 0, 255)  # warna shape detection
        img_draw, count_yellow = filter_contours_img(
            contours, img_draw, color_bbox)
        print('Red Count:', count_yellow)
        result_Yellow = cv2.bitwise_and(
            img, img, mask=mask_Yellow)

        # define range of hijau color in HSV
        lower_Orange = np.array([h_min2, s_min2, v_min2])  # 120 150 100
        upper_Orange = np.array([h_max2, s_max2, v_max2])  # 135 255 255
        mask_Orange = setRangeColor(imgHsv, lower_Orange, upper_Orange)
        contours = contours_img(mask_Orange)
        color_bbox = (0, 255, 0)  # warna shape detection
        img_draw, count_orange = filter_contours_img(
            contours, img_draw, color_bbox)
        print('Green Count:', count_orange)
        result_Orange = cv2.bitwise_and(
            img, img, mask=mask_Orange)

        # define range of biru color in HSV
        lower_Blue = np.array([h_min3, s_min3, v_min3])  # 180 100 100
        upper_Blue = np.array([h_max3, s_max3, v_max3])  # 255 255 255
        mask_Blue = setRangeColor(imgHsv, lower_Blue, upper_Blue)
        contours = contours_img(mask_Blue)
        color_bbox = (255, 0, 0)  # warna shape detection
        img_draw, count_blue = filter_contours_img(
            contours, img_draw, color_bbox)
        print('Blue Count:', count_blue)
        result_Blue = cv2.bitwise_and(
            img, img, mask=mask_Blue)

        # memberi text dan count pada window
        img_draw = draw_text_on_image(
            img_draw, count_yellow, count_orange, count_blue)

        # show image
        # cv2.imshow("Video", img)
        # cv2.imshow("ImageHsv", imgHsv)
        # cv2.imshow("Range Yellow", mask_Yellow)
        # cv2.imshow("Range Orange", mask_Orange)
        # cv2.imshow("Result Yellow", result_Yellow)
        cv2.imshow("Draw Image", img_draw)

        # image Stack
        imgBlank = np.zeros_like(img)
        imageStack = stackImages(0.4, ([img, imgHsv],
                                       [mask_Yellow, result_Yellow],
                                       [mask_Orange, result_Orange],
                                       [mask_Blue, result_Blue]))
        cv2.imshow("Image Stack", imageStack)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main2()
    cv2.waitKey(0)
