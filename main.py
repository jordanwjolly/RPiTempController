#!/usr/bin/python
#FUTURE WORK:   DONE: Have the WTI bash scripts run in the background (so it doesn't block main)
#               DONE: Fix the implementation of timestep in super loop. Is currently invalid
#               DONE: Put fancy spinning cursor while waiting for next time-step
#               DONE: Validate the timestep incrementing in real-time

#TO DO!!!!
#Fix up the temp logger file, has relance on old global vars
#               sub-plotting of output graphs/fix gross matplotlib graphing
#               Put function in BangBang class to get current temp automatically
#               Overhaul multi-sensor temperature driver... is super slow and silly. Make them run in parallel
#               Loose the pickle format

# LIBRARIES
import os, time, csv, sys, signal
#import numpy as np
from multiprocessing import Process
from Software_control import Controller
from Software_control import Data_logging
from Hardware_control import WTI_control
from Hardware_control import Temp_sensor
import config

# Static Variables
DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_TEMP_FILE = DIR + '/Hardware_control/SensorValues.txt'
GRAPH_DIR = DIR + '/Data_Logging/'
INITIALISE = config.initialisationVariables()    # Hack to bring vars in from config. breaks loop if config incorrect

if not INITIALISE.DUMMY:
    from Hardware_control import RPi_control

# Class which holds all temps/states/times
class TankVariables:

    def __init__(self, relay_id):
        self.Relay_ID = relay_id

    ERROR_TOLERANCE = INITIALISE.ERROR_TOLERANCE
    COOLER_RECOVERY_TIME = INITIALISE.COOLER_RECOVERY_TIME
    HEATER_RECOVERY_TIME = INITIALISE.HEATER_RECOVERY_TIME
    Current_Temp = float(0) # Should have function to retreive most current temp automatically
    Set_Temp = float(0)     # Set by controller
    Heater_State = False    # Current state
    Heater_Enable = False   # Future state
    Cooler_State = False
    Cooler_Enable = False
    Last_Heater_Enable = 0
    Last_Cooler_Disable = 0

#Allowing for graceful exit
def sigterm_handler(signal, frame):
    print('Exiting because of SIGTERM')
    sys.exit(0)

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def write_stdout(char_to_print):
    sys.stdout.flush()
    sys.stdout.write('\b')
    sys.stdout.write(char_to_print)

def time_step(current_time):
    return time.time() - current_time

def print_current_state(Relay_ID, Current_Temp, Set_Temp, Heater_State, Cooler_State):
    print ('TANK #' + str(Relay_ID)+ ": Curr=" + str(Current_Temp) + " Set=" + str(Set_Temp) + " Heat=" + str(Heater_State) + " Cool=" + str(Cooler_State))
    
# Main
def main():
   
    #Registering Handler
    signal.signal(signal.SIGTERM, sigterm_handler)

    #initialising each Tank object based of user input
    tank_list=[None, None, None, None, None, None, None, None]
    print("\nRUNNING PROGRAM WITH FOLLOWING TANKS: "+str(INITIALISE.TANK_ENABLE)+"\n")
    for indx, Tank_ID in enumerate(INITIALISE.TANK_ENABLE):
        tank_list[indx] = TankVariables(Tank_ID)
    
    #Sets up GPIO pins for pi. Forces all relays into off state. SHOULD START TEMP SENSOR HERE
    if not INITIALISE.DUMMY:
        RPi_control.setupGPIO()
        WTI_control.WTI_initialse(INITIALISE.TANK_ENABLE, DIR)#Need to initialise all relays into OFF state first        
        #Process(target=Temp_Sensor.start_temp_sensor(config.sensor_ID), args=(config.sensor_ID)).run() #starts temp sensor process

    # MAIN Super Loop
    TIME_STEP_THRESH = INITIALISE.REFRESH_TIME * len(INITIALISE.TANK_ENABLE)
    t=0

    while (t < INITIALISE.RUNTIME): #Is calculated in seconds, range time skip increases based of # of tanks

        current_time = time.time() #getting current time for TIME_STEP validation
        # Print nice output, ready for next graph
        print("\n#######################################################")

        # Loops through list of controller objects, updates controller, and actuates if needed
        for tank in tank_list:
           
            if tank == None: # None exists for all non-tanks
                continue

            # Updates current temperature
            tank.Current_Temp = Temp_sensor.current_temp(tank.Relay_ID)
            tank.Set_Temp = config.equations(tank.Relay_ID, t)

            # Checks state, to see if state change required
            tank.Heater_Enable, tank.Cooler_Enable = Controller.controller(tank.Set_Temp,
                                        tank.Current_Temp, tank.Heater_State, tank.Cooler_State, tank.ERROR_TOLERANCE)

            # Checks Validity of state change (based off hardware constraints)
            if Controller.HeaterCheck(tank.Heater_Enable, tank.Cooler_State, tank.Last_Heater_Enable, tank.HEATER_RECOVERY_TIME):
                tank.Heater_Enable = not tank.Heater_Enable

            if Controller.CoolerCheck(tank.Cooler_Enable, tank.Heater_State, tank.Last_Cooler_Disable, tank.COOLER_RECOVERY_TIME):
                tank.Cooler_Enable = not tank.Cooler_Enable

            # Controls hardware relays connected to the WTI ethernet switch
            if not tank.Heater_State == tank.Heater_Enable:

                WTI_control.WTI_logic(tank.Heater_Enable, DIR, tank.Relay_ID, INITIALISE.DUMMY) #Turn the relay on/off

                if not tank.Heater_State and tank.Heater_Enable: # updating last enable time
                    tank.Last_Heater_Enable = time.time()

                tank.Heater_State = tank.Heater_Enable #changing last state heater

            # Changes state of Cooler and actuates (If required)
            if not tank.Cooler_State == tank.Cooler_Enable:
                
                print("IF WE HAD A COOLER, I WOULD CHANGE THE STATE NOW")
                # WTI_control.WTI.logic(tank.Cooler_Enable, DIR, tank.Relay_ID,  DUMMY) #This will change a relay
                tank.Cooler_State = tank.Cooler_Enable #Updating last state of cooler
                
                if not tank.Cooler_Enable: # updating last disable time
                    tank.Last_Cooler_Disable = time.time()

            # Display current state
            print_current_state(tank.Relay_ID, tank.Current_Temp, tank.Set_Temp, tank.Heater_State, tank.Cooler_State)

            #Saves current values for tank 'x' to csv
            Data_logging.saveCurrentState(t, tank.Set_Temp, tank.Current_Temp, tank.Relay_ID, tank.Heater_State, tank.Heater_Enable, tank.Last_Heater_Enable,
                tank.Cooler_State, tank.Cooler_Enable, tank.Last_Cooler_Disable, GRAPH_DIR)

            # update GUI graph results
            if INITIALISE.GRAPH_SHOW:
                Data_logging.updateGraph(GRAPH_DIR, tank.Relay_ID)
                print("WOW...Graph")
         
        spinner=spinning_cursor() 

        TIME_STEP=time_step(current_time)

        while TIME_STEP < TIME_STEP_THRESH: #
            time. sleep(0.1)
            write_stdout(next(spinner))
            TIME_STEP = time_step(current_time)
        write_stdout(" ")

        # Updates t based off most current time delta
        t=t+ time_step(current_time)
	

###################################
if __name__ == "__main__":
    main()