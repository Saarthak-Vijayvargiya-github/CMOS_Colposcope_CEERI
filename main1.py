"""*************************************************************************************************
-> Data class and code for serial communication.
-> Data Variables:
    1. prevValue contains previous value of the contrast index denoted by "Previous"
    2. currValue contains the current value of the contrast index denoted by "Laplace".
    3. aFocus_status is status of AutoFocus. 3 status values: running it's 1, recording it's 2 otherwise 0.
    4. laplaceValues records the current values of laplace for calculating the position of maximum focus.
-> datavar is the object which stores the values.

-> initSerial() shows the list of available ports, asks the user to enter the COM number and 
initialises the port which has to be used for communication.
-> serialCommFocus() is run to read the value returned by arduino via port.
-> sendAutoFCommand() sends the command (currently set to "A") to the arduino to run autoFocusCheck() of the arduino.
-> autoFocus() takes the recorded laplace values, find it's max, and as the values are distributed within 75 loops
therefore calculates the loop no. in which value was maximum. Then that loop no. is sent to arduino.
(in this case 75 loops because total number of steps in stepper motor are 3009 and 40 steps are taken in one loop, so 
nearest int is 75, and if there are total of x entries in laplaceValues list and the max element is at the index y, then approx 
loop number out of 75 which has the max value would be [(y/x)*75])
*************************************************************************************************"""

import serial.tools.list_ports
import time
LOOPS = 75              # No. of loops taken by stepper motor for focus for full traversing of the lens.
AUTOF_COMMAND = "A"    # Command sent through serial port to arduino.

class Data:
    def __init__(self,prev,curr,aF_s):
        self.prevValue = prev
        self.currValue = curr
        self.aFocus_status = aF_s
        self.laplaceValues = []

    def info(self):
        print(f"Previous: {self.prevValue}  Laplace: {self.currValue}")
        
    def record(self,lVal):
        self.laplaceValues.append(lVal)
        

dataVar = Data(0,0,0)
serial_inst = serial.Serial()
status = 0

def initValues():
    dataVar.laplaceValues = []
    dataVar.aFocus_status = 0
    
def initSerial():
    ports = serial.tools.list_ports.comports()
    ports_list = []

    for port in ports:
        ports_list.append(str(port))
        print(str(port))
    
    val: str = input('Select Port: COM')
    for i in range(len(ports_list)):
        if ports_list[i].startswith(f'COM{val}'):
            port_var = f'COM{val}'
            print(port_var)

    serial_inst.baudrate = 9600
    serial_inst.port = port_var
    serial_inst.timeout = 0.01           # If this is increased, then speed of capturing will decrease
    serial_inst.open()

def serialCommFocus():
    global status
    status = serial_inst.read(size=1)
    try:
        return int(status)
    except:
        return 0

def sendAutoFCommand():
    value = AUTOF_COMMAND
    serial_inst.write(value.encode('utf-8'))
    dataVar.aFocus_status = 1
    time.sleep(0.5)

def autoFocus():
    max_value = max(dataVar.laplaceValues)
    max_index = dataVar.laplaceValues.index(max_value)
    focus_index = round(LOOPS * max_index/len(dataVar.laplaceValues))
    focus_index = str(focus_index)
    serial_inst.write(focus_index.encode('utf-8'))
    print("Total values recorded:", len(dataVar.laplaceValues),"Maximum Contrast Value:",max_value)
    print("Index in the list:", max_index,"\nLoop of the focus:", focus_index)
    time.sleep(0.05)
    # data = serial_inst.readline()
    # print("Loops:", data)