# coding: utf-8

"""
Created On:2016/6

@author:yyq
"""

import logic_process


class ClientPackage(object):
	def __init__(self, proto, pack_id):
		self._proto = proto
		self._pack_id = pack_id

	def Unpack(self, pack):
		seg = pack.UnpackByte()
		# seg = pack.UnpackWord()
		# seg = pack.UnpackDWord()
		# seg = pack.UnpackString()
		self.SetBack(seg, )

	def SetBack(self, *args):
		handle = logic_process.LogicHandle(arg1, arg2, self.Result)
		handle.Start()

	def Result(self, *args):
		"""
		result logic, prefer simple
		:param args:
		:return:
		"""
		self.Pack(sendpack, args)

	def Pack(self, sendpack, *args):
		sendpack.PackByte(arg1)
		sendpack.PackWord(arg2)
		sendpack.Send()
