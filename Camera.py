"""*************************************************************************************************
    IMP: Main program to be run. Press 'a' to autofocus and ESC to close the program.
-> Contatins code for camera and calculation of contrast index.
-> main1 contains the definitions of the class, variables and code for serial communication.
-> laplace() calculates the contrast index and stores in the dataVar variable.
-> frame is captured and stored as "open_cv_frame.png" in the same folder and shown in the Camera Footage window.
-> The frame is converted into GRAYSCALE for better accuracy and laplacian is run to calculate contrast index.

-> When 'a' is pressed, it will send the command to arduino and dataVar.aFocus_status is set to 1. Now aFocus_status
will read the value via port, and when 1 is detected dataVar.aFocus_status is set to 2 for recording values inside 
laplace(). When aFocus_status is 2, then autoFocus() calculates the loop which has maximum focus and sends
the loop number via port to the arduino. initValues() initialises the list of laplace and dataVar.aFocus_status
-> Basically dataVar.aFocus_status gets the status at the starting of operation and aFocus_status(local to file) 
records the status of completion.

****STATUS SHOWN BY VARIABLES****
1. So, when 'a' is pressed, this means you have to autofocus, dataVar.aFocus_status = 1 and aFocus_status remains at 0.
2. Lens is first moved in the outermost point and dataVar.aFocus_status = 2, aFocus_status = 1.
2. Program starts recording laplace values and lens is moved in inner direction. After lens is reached to the innermost 
point aFocus_status detects it's value as 2.
4. Recording stops and dataVar.aFocus_status = 0, aFocus_status = 0.
*************************************************************************************************"""

import cv2
import time
import main1 as m1

m1.initSerial()
camera = cv2.VideoCapture(0)
cv2.namedWindow("Python Webcam")
m1.initValues()
aFocus_status = 0

def laplace(img):
    time.sleep(0.01)
    m1.dataVar.prevValue = m1.dataVar.currValue
    m1.dataVar.currValue = cv2.Laplacian(img, cv2.CV_64F).var()
    m1.dataVar.currValue = round(m1.dataVar.currValue,2)
    # m1.dataVar.info()
    if m1.dataVar.aFocus_status == 2:
        m1.dataVar.record(m1.dataVar.currValue)
        # print(m1.dataVar.laplaceValues)


while True:
    ret,frame = camera.read()
    if not ret:
        print("Failed to grab Frame")
        break
    
    img_name = "open_cv_frame.png"
    cv2.imwrite(img_name,frame)
    cv2.imshow("Camera Footage",frame)
    img = cv2.imread(img_name,cv2.IMREAD_GRAYSCALE)
    laplace(img)
    # laplacian = cv2.Laplacian(img, cv2.CV_64F)                    # For showing laplacian
    # cv2.imshow("Laplacian Footage",laplacian)
    if m1.dataVar.aFocus_status == 1 or m1.dataVar.aFocus_status == 2:
        aFocus_status = m1.serialCommFocus()
    if aFocus_status == 1:
        m1.dataVar.aFocus_status = 2
        print("Recording Values...","Lens going to the last position")
    elif aFocus_status == 2:
        print("Calculating Best Position...")
        m1.autoFocus()
        print("Going to best position...")
        m1.initValues()
        aFocus_status = 0
    else: pass

    k = cv2.waitKey(1)
    if k & 0xFF == ord('a'):                            # Auto Focussing key
        m1.sendAutoFCommand()
        print("AutoFocus Triggered!","Lens going at starting position.")
    if k%256 == 27:                                     # ESC key
        print("Closing")
        break

camera.release()