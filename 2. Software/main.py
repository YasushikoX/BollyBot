import cv2
import numpy as np
import time
import serial

ser = serial.Serial('COM6', 9600)
time.sleep(2)

cap = cv2.VideoCapture(0)

cap.set(3, 1920) # Width
cap.set(4, 1080) # Height

lower_color = np.array([35, 30, 30])
upper_color = np.array([80, 255, 255])

left = "R,220\nL,160\n"
slow_left = "R,200\nL,180\n"
right = "R,160\nL,220\n"
slow_right = "R,180\nL,200\n"
stop = "R,188\nL,188\n"
forward = "R,250\nL,250\n"
back = "R,250\nL,250\n"

while True:
    line = ser.readline().decode('utf-8').strip()
    voltage = float(line)
    if voltage <= 11:
        print(voltage)
        print("LOW VOLTAGE")
        break
    else:   
        ret, frame = cap.read()

        if not ret:
            continue

        frame = cv2.resize(frame, (1280, 720))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_color, upper_color)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)
        mask = cv2.dilate(mask, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour
        if max_contour is not None:
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            center_x = x + w // 2
            center_y = y + h // 2
            if max_area > 500:
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), 2)
            else:
                cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), 2)
            
            width = frame.shape[1]

            line_position = int(width / 2)

            center_width = 55

            center_left = line_position - center_width
            center_right = line_position + center_width
            center_left_far = line_position - center_width * 2
            center_right_far = line_position + center_width * 2

            cv2.line(frame, (line_position, 0), (line_position, frame.shape[0]), (0, 0, 255), 2)
            cv2.line(frame, (center_left, 0), (center_left, frame.shape[0]), (255, 0, 0), 2)
            cv2.line(frame, (center_right, 0), (center_right, frame.shape[0]), (255, 0, 0), 2)
            cv2.line(frame, (center_left_far, 0), (center_right, frame.shape[0]), (255, 0, 0), 2)
            cv2.line(frame, (center_right_far, 0), (center_right, frame.shape[0]), (255, 0, 0), 2)

            if center_x < center_left:
                ser.write(slow_left.encode())
            elif center_x > center_right:
                ser.write(slow_right.encode())
            elif center_x < center_left_far:
                ser.write(left.encode())
            elif center_x > center_right_far:
                ser.write(right.encode())
            else:
                ser.write(stop.encode())
                time.sleep(2)
                ser.write(forward.encode())

        cv2.imshow('frame', cv2.resize(frame, (1920, 1080)))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
