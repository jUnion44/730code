import cv2
import numpy as np
from picamera2 import Picamera2
import time
import gpiozero
from threading import Thread
# from nptest import process_frame
from test import process_frame
from controls import *
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import os

factory = PiGPIOFactory()
# pwm_tilt = Servo(13, pin_factory=factory)#,min_pulse_width=0.5,max_pulse_width=2.6,frame_width=20)
# pwm_tilt.value = 1
pwm_button = Servo(12, pin_factory=factory)#,min_pulse_width=0.5,max_pulse_width=2.6,frame_width=20)
pwm_button.value = 0.5

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camera = Picamera2()
print("CAMERA ON")
camera_config = camera.create_preview_configuration()
camera.configure(camera_config)

# camera.resolution = (1024, 768)
camera.start()
print("CAMERA WARMED UP")
# Camera warm-up time
time.sleep(2)
print("CAMERA CAPTURE FILE")
camera.capture_file('foo.jpg')
# exit()
# cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def push_button():
    print("push")
    pwm_button.value = 0.9
    time.sleep(0.3)
    pwm_button.value = 0.5

last_hands = False
while True:
   
    frame = camera.capture_array()[:, :, :3]
    height,width,_ = frame.shape
    # print(width,height)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # if not ret:

    curr_hands = process_frame(frame)
    print(curr_hands)
    if curr_hands and not last_hands:
        push_button()
    last_hands = curr_hands
    #     break

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    frame = np.float32(frame)
    biggest_box = None
    max_area = 0
    # if len(faces) > 1:
    #     push_button()
    for (x, y, h, w) in faces:
        area = w*h
        if area > max_area:
            max_area = area
            biggest_box = (x + w//2, y + h//2)
        print(f"CENTER OF FACE IS {x + w//2, y + h//2}")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.circle(frame, biggest_box, 10, (255, 0, 255), 2)

    if biggest_box != None:
        # push_button()
        # time.sleep(0.3)
        width_p, height_p = biggest_box

        num_calls_table = round(abs((width/2) - width_p) / 10.3)
        num_calls_fan = round(abs((height/2) - height_p) / 9.8)
        if width_p > width/2:
            print(f"fan cw")
            print(f"TNUM: {num_calls_table}")
            for _ in range(num_calls_table):
                cw()
            # pwm_tilt.value = max(pwm_tilt.value-0.4,-0.6)
        else:
            print(f"fan ccw")
            print(f"TNUM: {num_calls_table}")
            for _ in range(num_calls_table):
                ccw()

        if height_p > height/2:
            print(f"tilt down")
            print(f"FNUM: {num_calls_fan}")
            for _ in range(num_calls_fan):
                down()
            # pwm_tilt.value = max(pwm_tilt.value-0.4,-0.6)
        else:
            print(f"tilt up")
            print(f"FNUM: {num_calls_fan}")
            for _ in range(num_calls_fan):
                up()
            # pwm_tilt.value = min(pwm_tilt.value+0.4,1)
    cv2.imwrite('output.png', frame)

    # time.sleep(0.1)
    # val = ""
    # pwm_tilt.value = float(val)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cap.release()
# cv2.destroyAllWindows()