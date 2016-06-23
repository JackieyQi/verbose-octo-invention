#coding: utf-8

"""
Created On:2016/6

@author:yyq
"""


class LogicHandle(object):
	def __init__(self, data_a, data_b, callback):
		self._data_a = data_a
		self._data_b = data_b
		self._callback = callback

	def Start(self):
		"""
		trans to other obj, and set callback
		"""
		self.Finish()

	def Finish(self, *args):
		"""
		:return to src
		"""
		self._callback(args)