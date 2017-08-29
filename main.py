# This will be the main program
# This is the main module that will pull components from the different tools into one
# program.  I will be easy to maintain and also to debug as it is just a testing 
# platform


# Import the required files
import mainTools	# RangeFinder, Alert, Tempeture
import time


#define class and methos
rangeTool = mainTools.range_finder()
ra = mainTools.remoteAlert()

# Steven's phone for a push
#  dev_id = 'REMOVED'
# Rachelle's phone
dev_id = ra.getKey()
myDev = ra.getKey()
print ("My Key: " + myDev)

while True:
	# Variables
	waterLevelAvg = 0
	print ("WATER LOGGED v0.1")
	for rangeAvg in range(0,5):
		waterLevelAvg = waterLevelAvg + rangeTool.find_range()

	# Might need to be refactored into it's own method in mainTools
	distanceFromWater = waterLevelAvg / (rangeAvg + 1)
	# Print the distance to console
	print ('Distance from water is: ' + str(distanceFromWater))

	# total length to bottom is 2 feet or 60.69cm
	if distanceFromWater >= 47:
		print (ra.send (dev_id, 'Low Water! You know what needs to be done!'))
	elif distanceFromWater >= 40:
		print (ra.send(dev_id, 'About half water left, consider giving me a few pints'))
	elif distanceFromWater >= 0:
				print (ra.send(dev_id, 'Test Notification - Boobs'))
	else:
		print ("Looking good, no notifications")
	time.sleep(14400)
