from io import BytesIO
from PIL import Image

import sqlite3
import cv2
import os

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
        self.db = sqlite3.connect('main.db')
        self.cursor = self.db.cursor()

        self.collage_name = collage_name
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {0}_members (
                            fio CHAR(255),
                            grup CHAR(255)
                        )'''.format(self.collage_name))
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {0}_info (
                            fio CHAR(255),
                            grup CHAR(255),
                            path_to_img TEXT,
                            dute DATETIME
                        )'''.format(self.collage_name))
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {0}_cash (
                            fio CHAR(255),
                            grup CHAR(255),
                            frame BLOB,
                            dute DATETIME
                        )'''.format(self.collage_name))
        self.db.commit()

    def add_user(self, fio, grup):
        self.cursor.execute('INSERT INTO {0}_members VALUES (?, ?)'.format(self.collage_name), (fio, grup))
        self.db.commit()

    def add_cash(self, fio, grup, frame, date):
        self.cursor.execute('INSERT INTO {0}_cash VALUES (?, ?, ?, ?)'.format(self.collage_name), (fio, grup, frame, date))
        self.db.commit()

    def found_data_in_db(self, data: str):
        for fio, grup in self.cursor.execute('SELECT * FROM {0}_members'.format(self.collage_name)).fetchall():
            f, g = data.split(', ')
            if fio == f and g == grup:
                return True
        return False

    def pop_cash(self):
        cash = self.cursor.execute('SELECT * FROM {0}_cash'.format(self.collage_name)).fetchall()
        self.cursor.execute('DELETE FROM {0}_cash'.format(self.collage_name))
        self.db.commit()

        for data in cash:
            yield data

    def add_row(self, fio, grup, frame, date):
        if frame:
            path = os.path.join(os.getcwd(), f'imgs/{str(next(gener))}.jpg')
            cv2.imwrite(path, frame)
        else:
            path = 'None'

        self.cursor.execute('INSERT INTO {0}_info VALUES (?, ?, ?, ?)'.format(self.collage_name), (fio, grup, path, date))
        self.db.commit()


def init_db(collage_name: str):
    return Collage_manager(collage_name)