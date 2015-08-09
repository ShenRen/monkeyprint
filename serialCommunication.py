#!/usr/bin/python
# -*- coding: latin-1 -*-

import serial
import printSettings

class serialPrinter:

	def __init__(self, settings):
		self.settings = settings
		# Configure serial.
		self.serial = serial.Serial(
			port='/dev/ttyACM0',
			baudrate=9600,
			bytesize = serial.EIGHTBITS, #number of bits per bytes
			parity = serial.PARITY_NONE, #set parity check: no parity
			stopbits = serial.STOPBITS_ONE,
			timeout = 0
		)
		
	# Commands.
	def buildHome(self):
		self.serial.write("buildHome")
		self.waitForAckInfinite()
		
	def buildBaseUp(self):
		while 1:
			self.serial.timeout = 5
			self.serial.write("buildBaseUp")
			printerResponse = self.serial.readline()           # Wait for 5 sec for anything
			print "PRINTER RESPONSE: " + printerResponse
			printerResponse = printerResponse.strip()
			if printerResponse == "done":
				break
			else:
				print "      No response from printer. Resending command..."
		self.serial.timeout = None


		
	def buildUp(self):
		while 1:
			self.serial.write("buildUp")
			self.serial.timeout = 5
			printerResponse = self.serial.readline()           # Wait for 5 sec for anything
			print "PRINTER RESPONSE: " + printerResponse
			printerResponse = printerResponse.strip()
			if printerResponse == "done":
				break
			else:
				print "      No response from printer. Resending command..."
		self.serial.timeout = None
		
	def buildTop(self):
		self.serial.write("buildTop")
		self.waitForAckInfinite()
		
	def tilt(self):
		self.serial.write("tilt")
		self.waitForAckInfinite()
		
	def setStart(self):
		self.serial.write("printingFlag 1")
		
	def setStop(self):
		self.serial.write("printingFlag 0")
		
	# Settings.
	def setLayerHeight(self):
		self.serial.write("buildLayer " + str(self.settings.getLayerHeight() * self.settings.getStepsPerMm()))
		
	def setBaseLayerHeight(self):
		self.serial.write("buildBaseLayer " + str(self.settings.getBaseLayerHeight() * self.settings.getStepsPerMm()))
		
	def setBuildSpeed(self):
		self.serial.write("buildSpeed " + str(self.settings.getBuildSpeed))
			
	def setTiltSpeedSlow(self):
		self.serial.write("tiltSpeed " + str(self.settings.getTiltSpeedSlow))

	def setTiltSpeedFast(self):
		self.serial.write("tiltSpeed " + str(self.settings.getTiltSpeedFast))
		
	def setTiltAngle(self):
		self.serial.write("tiltAngle " + str(self.settings.getTiltAngle))
		
	def setNumberOfSlices(self, numberOfSlices):
		self.serial.write("nSlices " + str(numberOfSlices))
		
	def setCurrentSlice(self, currentSlice):
		self.serial.write("slice " + str(currentSlice))
	
#	def setTimeout(self, timeout):
#		self.serial.timeout = timeout	# Timeout for readline command. 0 is infinity, other values are seconds.

#	def waitForAckFinite(self,timeout):
#		self.serial.timeout = timeout
#		printerResponse = self.serial.readline()           # Wait for 5 sec for anything
#		print "PRINTER RESPONSE: " + printerResponse
#		printerResponse = printerResponse.strip()
#		if printerResponse=="done":
#			return 1
#		elif printerResponse != "done":
#			print "Got strange response from printer: " + printerResponse
#			return 0
#		elif printerResponse == ""
#			return 0


	def waitForAckInfinite(self):
		print "waitForAck"
		self.serial.timeout = None
		printerResponse = self.serial.readline()           # Wait forever for anything
		print "PRINTER RESPONSE: " + printerResponse
		printerResponse = printerResponse.strip()
		if printerResponse=="done":
			return "done"
		elif printerResponse != "done":
			print "Got strange response from printer: " + printerResponse
			return None
		else:
			return None

	
	def ping(self):
		self.serial.write("ping")
		self.serial.timeout = 10
		printerResponse = self.serial.readline()           # Wait forever for anything
		printerResponse = printerResponse.strip()
		if printerResponse!="ping":
			return 0
		else:
			return 1
			
	def close(self):
		self.serial.close()
#		print "printer serial closed"


#dontNeedThis = serialPrinter.flushInput()		

class serialProjector:

	def __init__(self):
		self.serial = serial.Serial(
			port='/dev/ttyUSB0',
			baudrate=9600,
			bytesize = serial.EIGHTBITS, #number of bits per bytes
			parity = serial.PARITY_NONE, #set parity check: no parity
			stopbits = serial.STOPBITS_ONE
	)
	
	def activate(self):
		self.serial.write("* 0 IR 001"+'\r')

	def deactivate(self):
		self.serial.write("* 0 IR 002"+'\r')

	def close(self):
		self.serial.close()
#		print "projector serial closed"
