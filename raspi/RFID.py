import RPi.GPIO as GPIO
import MFRC522python.MFRC522 as MFRC522
import signal

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

def getUid():
    
    while True:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            # Print UID
            return "%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]) 

