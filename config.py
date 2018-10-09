#!/usr/bin/python

# This file contains all equations that a user can change
# It's method of returning initialisation vars is bad practise, but is appropriate for the user
# A user needs to input the Sensor IDs themselves
import math

# Change the variables listed below as required by the experiment
class initialisationVariables:
    TANK_ENABLE = [1, 2]  # Specifies which equations/tanks we wish to use, remove numbers as needed
    ERROR_TOLERANCE = 0.05                  # Allowable temperature error tolerance
    RUNTIME = 1                             # Run time of experiment (Is specified in hours)
    GRAPH_SHOW = True                       # Toggle True/False to show graphical output of temp profile
    TIME_STEP = 5                           # Refresh rate of system (Seconds))
    COOLER_RECOVERY_TIME = 60
    HEATER_RECOVERY_TIME = 10


# The Equations for our eight water tanks.
# To change the equation for a specifc relay, change the return value
# A more natural language reading of the function is " for a given relayID, return the set temperature for a given 't' "
def equations(relayID, t):
    t = float(t)  # casting to float (saftey)

    # Uncomment for every tank in use
    if relayID == 1:
        return 28 - (t / 2)          # equation 1

    elif relayID == 2:
        return 28 + (math.cos(t) * 4)  # equation 2

    elif relayID == 3:
        return 10 - (t / 2)  # equation 3

    elif relayID == 4:
        return 7 + (2 * t)  # equation 4

    elif relayID == 5:
        return 28 + (t / 2)  # equation 5

    elif relayID == 6:
        return 28 + (t / 2)  # equation 6

    elif relayID == 7:
        return 28 + (t / 2)  # equation 7

    elif relayID == 8:
        return 28 + (t / 2)  # equation 8
    else:
        return False

# This function returns the hardcoded addresses of the temperature sensors
# NOTE: keeping with convention, index starts at '1'.
# Sensor 1 for tank 1, is in the first place etc...
def sensor_ID():

    s1 = "28-000006dc6863"
    s2 = "28-000006dc76f3"
    s3 = None
    s4 = None
    s5 = None
    s6 = None
    s7 = None
    s8 = None

    sensorID = [s1, s2, s3, s4, s5, s6, s7, s8]
    return sensorID
