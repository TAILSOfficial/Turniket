from flask import Flask, request, render_template
from loguru import logger

import threading
import asyncio
import socket
import pickle
import struct
import db


clients = {}

async def handle_client(client, addr):
	global clients

    payload_size = struct.calcsize('Q')
    loop = asyncio.get_event_loop()
    collage = None
    request = None
    data = b''
    while request != b'quit':
    	while len(data) < payload_size:
			packet = await loop.sock_recv(client, 4 * 1024) # 4K
			if not packet:
				break
			data += packet
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("Q", packed_msg_size)[0]
		while len(data) < msg_size:
			data += await loop.sock_recv(client, 4 * 1024)
		frame_data = data[:msg_size]
		data = data[msg_size:]
		frame = pickle.loads(frame_data)
		if type(frame) == str:
			command, *args = frame.split(' ')
			if command == 'SET_COLLAGE' and not collage:
				collage = args[0]
				clients[collage] = client

		elif type(frame) == tuple:
			db.init_db(collage).add_row(*frame)

async def main():
	global clients

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('', 5723))
	server.listen(900)

	loop = asyncio.get_event_loop()

	while True:
		a = await loop.sock_accept(server)
		loop.create_task(handle_client(*a))


app = Flask(__name__)

@app.route('/')
def mainpage():
	