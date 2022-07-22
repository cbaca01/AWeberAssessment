import sqlite3


class DBConnect(object):
	
	connection = None
	cur = None

	def __init__(self):
		self.connection = sqlite3.connect('WidgetsDB.db')
		self.cur = self.connection.cursor()


	def exe(self, query, params):
		self.cur.execute(query, params)
		return self.cur


	def last_row_id(self):
		return self.cur.lastrowid


	def get_results(self):
		results = []
		for r in self.cur.fetchall():
			results.append(r)
		return results


	def commit(self):
		self.connection.commit()


	def close(self):
		self.connection.close()