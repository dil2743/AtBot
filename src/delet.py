import serial
import time

locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',
'/dev/ttyACM0','/dev/ttyACM1','/dev/ttyACM2','/dev/ttyACM3']  
  
for device in locations:  
	try:  
		print "Trying...",device
		arduino = serial.Serial(device, 9600) 
		break
	except:  
		print "Failed to connect on",device   

try:  
    arduino.write('Y')  
    time.sleep(1)
    print arduino.readline()
except:  
    print "Failed to send!" 