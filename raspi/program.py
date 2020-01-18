import sqlite3
import time
import RPi.GPIO as GPIO
import RFID
import serial
import MFRC522python.MFRC522 as MFRC522
import signal


ledPin = 11
doorPin = 12


# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

def getData():
    while True:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        #If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Print UID
            return "%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])

        ser = serial.Serial(port = '/dev/ttyAMA0',baudrate = 9600,parity = serial.PARITY_NONE,stopbits = serial.STOPBITS_ONE,bytesize = serial.EIGHTBITS)
        if ser.in_waiting != 0:
            print("&&&")
            global doorType
            data = ser.readline()
            print("_"+data+"_")
            ser.close()
            if data=='Open\n':
                doorType = 1
                print("***")
            elif data=='Close\n':
                doorType = 0
                print("===")
        
        ser.close()

def sqlTool(query):
    sqlCon = sqlite3.connect("/home/pi/doorlock/raspi/access.db")
    result = sqlCon.cursor()
    result.execute(query)
    sqlCon.commit()
    return result.fetchall()

def doorControl(status):
    ser=serial.Serial('/dev/ttyAMA0',9600,timeout=0.5)
    if status == 0:
        #close door
        print 'lock door'
        ser.write('ClOsE')
    elif status == 1:
        #open door
        print 'open door'
        ser.write('OpEn')
    else:
        pass
    time.sleep(1.5)
    data = ser.readline()
    print(data)
    ser.close()

def findCard(Uid):
    query = "SELECT * FROM Card,Person WHERE owner = Id and Uid='{id}' and Status = 1".format(id=Uid)
    list = sqlTool(query)
    if not list:
        return False
    else:
        return True

def gpioSetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin,GPIO.OUT)


doorType = 0
# doorType = 0: Door close
# doorType = 1: Door open

def accessControl():
    global doorType
    uid = getData()
    query = "INSERT INTO Log(Uid, DateTime) VALUES(\'%s\', \'%s\');" % (uid,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print query
    sqlTool(query)
    if findCard(uid):
        print "fine Card"
        if doorType == 0:
            print "+++"
            doorType = 1
        else:
            print "---"
            doorType = 0
        doorControl(doorType)
    else:
        print "Unfind Card"




def main():
    while True:
        accessControl()

if __name__=='__main__':
    print "Hello! NTUST_CSIE_SO DoorLock System"
    #setup
    gpioSetup()
    #process
    main()
