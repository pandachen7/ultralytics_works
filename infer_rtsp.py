import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture('rtsp://admin:123456@192.168.0.201:554/profile1')
    while True:
        ret, image = cap.read()

        if ret:
            cv2.imshow('image_display', image)
            cv2.waitKey(1)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()