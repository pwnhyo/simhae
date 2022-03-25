from flask import request
from random import shuffle
from config import *

import time

def user_login(username, password) :
	conn = connect_db()

	conn.row_factory = dict_factory
	c = conn.cursor()

	query = 'select * from users where username=? and password=?'
	c.execute(query, (username, password,))
	result = c.fetchone()

	c.close()

	if result :
		return result

	return False


def user_register(username, password, email , phone , rate) :
	conn = connect_db()
	c = conn.cursor()

	query = 'select * from users where username=?'
	c.execute(query, (username,))
	result = c.fetchone()

	if result : # already exists
		return False


	query = 'insert into users values (?, ?, ?, ?, ?)'
	c.execute(query, (username, password, email , phone, rate))
	conn.commit()

	c.close()
	return True

def user_write(locate, title, contents, user_status, username) :
	conn = connect_db()
	c = conn.cursor()

	status = 1 # 1 is open

	query = 'insert into board values (NULL, ?, ?, ?, ?, ?, ?, ?, "")'
	c.execute(query, (locate, title, contents, user_status, username, status, time.time()))
	conn.commit()
	c.close()

	return True

def get_orders_from_db() :
	conn = connect_db()

	conn.row_factory = dict_factory
	c = conn.cursor()

	query ='select * from board order by no desc;'
	c.execute(query)
	data = c.fetchall()

	c.close()
	return data


def get_one_boorder_from_db(no) :
	conn = connect_db()

	conn.row_factory = dict_factory
	c = conn.cursor()

	query ='select * from board where no = ?;'
	c.execute(query,(no,))
	data = c.fetchone()

	c.close()
	return data
