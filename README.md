SUMMARY

This is a basic bang-bang temperature controller used for maintaining desired tempreatures in up to 8 seperate aquatic environments simultaneously.
It can be used to both heat, and cool an environment based off a desired temperature profile curve.

The system uses the following sensors/actuators:

	- Waterproof DS18B20 Digital temperature sensor for environmental sensing
	- Heating element
	- Cooling element
	- Network Power Switch from WTI

Where multiple water sources are required to be heated/cooled simatenously, a single cooler, heater, and tempreature sensor will be required per tank. 
A single setwork power switch is all thats required.

User options:

- A user can toggle a gui graph of temperature history turning on/off
- The desired curve can be edited by changing the equation in temperature_profile.py

GENERAL USER USE

Temperature sensors:
As the DS18B20 temperature sensor is a 1-wire device, as many of these sensors can all be connected to the same pull-up resistor circuirty
It is best if a user connects each of the sensors once at a time, and notes the unique sensor ID address.

User navigates to here:

cd /sys/bus/w1/devices/

Notes down the sensor ID, physically labels the sensor with a number 1-8, and then copies the sensor ID to the correspeonding slot in Temp_sensor.py


User specified temp:
User inputs the temprature_profile.py script


TO GET SOFTWARE RUNNING

Open up a terminal on the raspberry pi.

change directories "cd /RaspberryPiThermostat/Hardware_control"

run "python Temp_sensor.py"


....your temprature sensors are now running!!

change directories "cd /RaspberryPiThermostat/"

run "python temperature_profile.py"


...everything is now running!!!!!!!!!!!!!!!
