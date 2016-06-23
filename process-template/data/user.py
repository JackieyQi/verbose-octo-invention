# coding: utf-8

"""
Created On:2016/6

@author:yyq
"""

g_user = None
class User(object):
	def __init__(self):
		self._id = 0
		self._name = ''
		self._number = ''
		self._phone = ''

	def SetItems(self):
		pass


g_allusers = None
class AllUsers(object):
	def __init__(self):
		self._ids = {}

	def Set(self, *args):
		pass

	def Get(self, *args):
		pass
