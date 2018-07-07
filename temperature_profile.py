#!/usr/bin/python
# USE: 	This file runs the temperature profile curve. 
#	
#	To edit the curve, change the equation labeled below as "The Equation"

# LIBRARIES
import os, time, math
from Software_control import Actuator_control
from Software_control import Graph_show

# STATIC VARS
ERROR_TOLERANCE = 0.1	#Allowable temperature error tolerance
RUNTIME = 1 		#Run time of experiment (Is specified in hours)
GRAPH_SHOW= True	#Toggle True/False to show graphical output of temp profile
TIME_STEP = 5 #seconds step


# FILE PATH INFO
DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR+'/current.json'
SENSOR_SCRIPT_FILE = DIR + '/Hardware_control/Temp_sensor.py'
GRAPH_FILE = DIR + '/Software_control/Graph_values.csv'

# Sets up everything
Actuator_control.setupGPIO()

# Range of time
for t in range(0, RUNTIME*60*60):

	# The Equation
	setTemp = 22+2*math.cos(float(t)/2) #temperature

	# Get current Temperature
	currTemp = Actuator_control.currTemp(CURRENT_TEMP_FILE)

	# Does all of the stuff
	Actuator_control.checkClimate(ERROR_TOLERANCE, setTemp, currTemp, DIR) #first number is allowable temp diff. Second number is set temp

	# Update graph
	if (GRAPH_SHOW): 
		Graph_show.updateGraph(setTemp, currTemp, GRAPH_FILE)
	
	# Sets delay between reading intervals (should be larger than 5 seconds)
	time.sleep(TIME_STEP)

# Turns off everything at end of experiment
Actuator_control.goodbye()
