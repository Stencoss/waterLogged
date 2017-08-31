# This will hold definations of the main tools that will be used.
# These tools will be used by main.py
# Tools to include:
# 1) RangeFinder - Whats the current distance - single measurement return
# 	1a) RangeLowWater - Is this less than a set value
# 2) tempHum - This lets us test the temp and the hum level at the current sensor
# 3) remoteAlert - This sends a noticiation to the phone of a person 


import RPi.GPIO as GPIO		# Needed to check and read GPIO pins on pi
import time					# Needed for time, date, sleep
import json					# Needed for remoteAlert notifcations
import urllib2

# Range finder class Sets the GPIO pins to correct pins and then activates the
# ultrasonic sensors.  It rcvs two values that it then coverts into cm (Formula 
# was sourced by Adafruit).  It's return value is the distance from the sensor
# to where it is pointing.  Eventually to be on top of the water.

class range_finder():
	def find_range(self):
		# Sets up pins to be read by the rPi
		GPIO.setmode(GPIO.BCM)	# Tells how the pins are going to be labled
		TRIG = 23		# Sets pin for trig output on ultrasonic device
		ECHO = 24 		# Sets echo pin to 24 on ultrasonic device
		GPIO.setup(TRIG, GPIO.OUT)	# Assigns physical pin to 23 (TRIG) OUT
		GPIO.setup(ECHO, GPIO.IN)	# Assigns physical pin to 24 (ECHO) IN

		# Print to let the user know the readings and setup is starting
		time.sleep(.5)
		# Check the range
		try:

			GPIO.output(TRIG, True)
			time.sleep(.00001)
			GPIO.output(TRIG, False)
			# Sends and Rcvs signal.  Tracks in start and stop
			while GPIO.input(ECHO)==0:
				pulse_start = time.time()
			# Echo in - high
			while GPIO.input(ECHO)==1:
				pulse_end = time.time()

			# Calculates the distance by using a time interval
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)

			# Distance is formatted into centimeters
			return distance
		# user ctrl + C to quit the function as it is running
		except KeyboardInterrupt:
			return '\nProgram was ended by the user\n'
		# defualt except - Something went wrong
		except:
			return '\nMust have been a bug\n'
		# Clean up all the pins once it is done
		finally:
			GPIO.cleanup()

	# This will take the current average value and check to see what level it
	# is at.  I will have different return values based on soon to be set value
	# Less then 0 = -1
	# Between 0 and 5cm = 0
	# Between 5.1 and 20.0 = 1
	# Greater than 20.0 = 2

	def range_Low_Water(self, avgDistance, times):

		avgDistance = avgDistance / times
		print (avgDistance)
		if avgDistance <= 0:
			return -1

		elif avgDistance > 0 and avgDistance <= 5:
			return 0

		elif avgDistance > 5 and avgDistance <= 20:
			return 1

		elif avgDistance > 20:
			return 2
		else:
			return 000

	# This class will save the value to file.  This is a work around for 
	# sending it to the second pi.... maybe we should keep it on one though
	# might be easier
	def sendToFile(self, waterValue):
		f = open('')

	# Placeholder for percent class this will take the measurement from rangefinder and 
	# use the equation 1 - [((range) - 23) / 36] = percent remaining.  It will have to
	# account for negative numbers and also 0.  Both which would be errors.  It should
	# be directly intergrated into waterLogged GUI 



class remoteAlert:
	def send(self, device_id, message):
		data = {'message': message}
		url = 'http://remote-alert.herokuapp.com/post/' + device_id
		req = urllib2.Request(url)
		req.add_header('Content-Type', 'application/json')
		urllib2.urlopen(req, json.dumps(data))
		return 'OK'

	#ra = RemoteAlert()
	dev_id = '60a0a796-4567-4f72-8adb-ab2e05eb1e00'

	def getKey(self):
		file = open('config/config', 'r')
		key = file.readline()
		file.close()
		return key



