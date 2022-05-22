from loguru import logger
from rich import print

import threading
import datetime
import socket
import pickle
import struct
import cv2
import db


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
payload_size = struct.calcsize("Q")
detector = cv2.QRCodeDetector()
cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)
MY_COLLAGE = 'KTSK'
db.init_db(MY_COLLAGE)

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
	global net_success, client, payload_size

	if net_success:
		while True:
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
	client.connect(('', 5723))
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

while True:
    cam_success, img = cam0.read()

    if not cam_success:
    	break

    data, bbox, _ = detector.detectAndDecode(img)
    
    if (bbox is not None):
        for i in range(len(bbox)):
        	print(bbox)
            a = tuple([int(k) for k in bbox[i][0]])
            b = tuple([int(k) for k in bbox[(i+1) % len(bbox)][1]])
            cv2.line(img, a, b, color = (255, 0, 0), thickness = 2)

        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        if db.found_data_in_db(data):
        	threading.Thread(target = send_data, args = (data, cam1.read())).start()
        	# put it

    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        break

if not cam_success:
	img = cv2.imread('Error.png')
	while True:
		cv2.imshow("Error!", img)

		if cv2.waitKey(1) == ord("q"):
    		break

cam0.release()
cam1.release()
cv2.destroyAllWindows()