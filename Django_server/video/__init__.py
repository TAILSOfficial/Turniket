from ..main.models import INFO

import threading
import asyncio
import struct
import socket
import zlib
import sys


async def handle_client(client, addr):
	loop = asyncio.get_event_loop()
    college = None
    request = None
    data = b''
    while request != b'quit':
    	while len(data) < 8:
			packet = await loop.sock_recv(client, 4 * 1024)
			if not packet:
				break
			data += packet
		packed_msg_size = data[:8]
		data = data[8:]
		msg_size = struct.unpack("Q", packed_msg_size)[0]
		while len(data) < msg_size:
			data += await loop.sock_recv(client, 4 * 1024)
		frame_data = zlib.decompress(data[:msg_size])
		data = b''
		command, *args = pickle.loads(frame_data)
		if command == 'SET_COLLEGE' and not college:
			college = args[0]
			sys.Colleges_frames.update({college: None})
			sys.Colleges_frames.update({college + '_sock': client})
		elif command == 'ADD_INFO':
			INFO(college = college, **args[0]).save()
		elif command == 'UPDATE_FRAME'
			sys.Colleges_frames.update({college: args[0]})

	del sys.Colleges_frames[college]

async def start_request_server(ip: str, port: int):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((ip, port))
	server.listen(1000)
	loop = asyncio.get_event_loop()

	while True:
		loop.create_task(handle_client(*loop.sock_accept())) 

def servers():
	if hasattr(sys, 'Colleges_frames'):
		setattr(sys, 'Colleges_frames', {})

	asyncio.run(start_request_server('0.0.0.0', 5427))

threading.Thread(target = servers).start()