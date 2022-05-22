from datetime import datetime
from loguru import logger

import MySQLdb
import sqlite3

try:
	cnx = MySQLdb.connect(user='root', password='',
						  host='localhost', database='skud')
	cursor = cnx.cursor()
	scheme = 'MySQL'
except Exception as e:
	logger.exception(e)
	cnx = sqlite3.connect('db.sqlite3')
	cursor = cnx.cursor()
	scheme = 'SQLite3'

@logger.catch
def get_members_dict() -> dict[str, str]:
	if scheme == 'MySQL':
		cursor.execute('SELECT * FROM `video_data`')
		return {i: j for i, j in cursor.fetchall()}
	elif scheme == 'SQLite3':
		return {i: j for i, j in cursor.execute('SELECT * FROM video_data').fetchall()}
	else:
		logger.error('what the fuck this scheme? "' + scheme + '"')

@logger.catch
def log_in_db(grup: str, name: str, path: str, date: datetime) -> None:
	if scheme == 'MySQL':
		cursor.execute('INSERT INTO `video_enter` (`id`, `grup`, `name`, `path_to_image`, `mega_date`) VALUES (NULL, %s, %s, %s, %s);', (grup, name, path, date))

	elif scheme == 'SQLite3':
		cursor.execute('INSERT INTO video_enter VALUES (NULL, ?, ?, ?, ?)', (grup, name, path, date))

	else:
		logger.error('what the fuck this scheme? "' + scheme + '"')

	cnx.commit()