#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import random

# Classe Pai
class Uart(object):

	def __init__(self, comport, baudrate):
		self.__comport = comport
		self.__baudrate = baudrate

	def getComport(self):
		return self.__comport

	def getBaudRate(self):
		return self.__baudrate

	def getTime(self):
		return datetime.datetime.now()

	def getRandom(self):
		return random.randint(0,100)

# Classe filha		
class Serial(Uart): 
	def __init__(self, comport, baudrate):
		super(Serial, self).__init__(comport, baudrate)