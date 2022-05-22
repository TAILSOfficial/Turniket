from io import BytesIO
from PIL import Image

import sqlite3
import cv2
import os

db = sqlite3.connect('main.db')
cursor = db.cursor()
collages = {}

def pathgen():
	i = 0
	while True:
		yield i
		i += 1
gener = pathgen()
for i in os.listdir('imgs'):
	next(gener)

class Collage_manager:
	def __init__(self, collage_name: str):
		global cursor, db

		self.collage_name = collage_name
		cursor.execute('''CREATE TABLE IF NOT EXISTS {0}_members (
							fio CHAR(255),
							grup CHAR(255)
						);
						CREATE TABLE IF NOT EXISTS {0}_info (
							fio CHAR(255),
							grup CHAR(255),
							path_to_img TEXT,
							dute DATETIME
						);
						CREATE TABLE IF NOT EXISTS {0}_cash (
							fio CHAR(255),
							grup CHAR(255),
							frame BLOB,
							dute DATETIME
						)'''.format(self.collage_name))
		db.commit()

	def add_user(self, fio, grup):
		global cursor, db

		cursor.execute('INSERT INTO {0}_members VALUES (?, ?)'.format(self.collage_name), (fio, grup))
		db.commit()

	def add_cash(self, fio, grup, frame, date):
		global cursor, db

		cursor.execute('INSERT INTO {0}_cash VALUES (?, ?, ?, ?)'.format(self.collage_name), (fio, grup, frame, date))

	def pop_cash(self):
		global cursor, db

		cash = cursor.execute('SELECT * FROM {0}_cash'.format(self.collage_name)).fetchall()
		cursor.execute('DELETE FROM {0}_cash'.format(self.collage_name))
		db.commit()

		for data in cash:
			yield data

	def add_row(self, fio, grup, frame, date):
		global cursor, db

		if frame:
			path = os.path.join(os.getcwd(), f'imgs/{str(next(gener))}.jpg')
			cv2.imwrite(path, frame)
		else:
			path = 'None'

		cursor.execute('INSERT INTO {0}_info VALUES (?, ?, ?, ?)'.format(self.collage_name), (fio, grup, path, date))
		db.commit()


def init_db(collage_name: str):
	global collages

	if collage_name not in collages.keys():
		collages.update({collage_name: Collage_manager(collage_name)})

	return collages[collage_name]