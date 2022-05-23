from loguru import logger
from rich import print

import RPi.GPIO as GPIO
import threading
import datetime
import socket
import pickle
import struct
import atexit
import time
import cv2
import db


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5)
payload_size = struct.calcsize("Q")
detector = cv2.QRCodeDetector()
cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)
MY_COLLAGE = 'KTSK'
db.init_db(MY_COLLAGE)
NOT_STOP = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
atexit.register(GPIO.cleanup)

def go_away():
    GPIO.output(23, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(23, GPIO.LOW)

def send_data(data: str, cast: tuple[bool, "numpy.ndarray"], date = datetime.datetime.now()):
    global net_success

    if cast[0]:
        frame = pickle.dumps(cast[1])
    else:
        frame = None

    if net_success:
        sig = pickle.dumps((*data.split(', '), frame, date))
        client.send(struct.pack('Q', len(sig)) + sig)
    else:
        db.init_db(MY_COLLAGE).add_cash(*data.split(', '), frame, date)

def add_new():
    global net_success, client, payload_size, NOT_STOP

    if net_success:
        while NOT_STOP:
            data = client.recv(4 * 1024)
            while len(data) < payload_size:
                packet = client.recv(4 * 1024) # 4K
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            db.init_db(MY_COLLAGE).add_user(*frame)

try:
    client.connect(('192.168.0.127', 5723))
    msg = pickle.dumps('SET_COLLAGE KTSK')
    client.send(struct.pack('Q', len(msg)) + msg)
    net_success = True

    for msg in db.init_db(MY_COLLAGE).pop_cash():
        _ = pickle.loads(msg[2])
        a = ', '.join((msg[0], msg[1]))
        b = (bool(_), _)
        send_data(a, b, date = msg[3])

    threading.Thread(target = add_new).start()

except Exception as e:
    logger.exception(e)
    net_success = False

def mega_qr():
    global img, NOT_STOP, detector
    
    my_db = db.init_db(MY_COLLAGE)
    
    while NOT_STOP:
        # t = time.time()
        data, bbox, _ = detector.detectAndDecode(img)
        # print(time.time() - t)
    
        if (bbox is not None) and data != '':
            for i in range(len(bbox)):
                a = tuple([int(k) for k in bbox[i][0]])
                b = tuple([int(k) for k in bbox[(i+1) % len(bbox)][1]])
                cv2.line(img, a, b, color = (255, 0, 0), thickness = 2)

            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            if my_db.found_data_in_db(data):
                threading.Thread(target = send_data, args = (data, cam1.read())).start()
                go_away()

cam_success, img = cam0.read()
if cam_success:
    threading.Thread(target = mega_qr).start()

while cam_success:
    cam_success, img = cam0.read()

    if not cam_success:
        break

    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        NOT_STOP = False
        break

if not cam_success:
    cv2.destroyAllWindows()
    img = cv2.imread('error.png')
    while True:
        cv2.imshow("Error!", img)

        if cv2.waitKey(1) == ord("q"):
            break

cam0.release()
cam1.release()
NOT_STOP = False
time.sleep(1)
cv2.destroyAllWindows()