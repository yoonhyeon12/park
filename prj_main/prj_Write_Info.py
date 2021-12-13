import RPi.GPIO as GPIO
from SimpleMFRC522 import SimpleMFRC522

mfrc = SimpleMFRC522()

try:    
    txt1 = input('input card name:')
    txt2 = input('input car num:')
    txt3 = input('input dscnt:')
    
    print("Now place your tag to write")
    
    mfrc.write_block(txt1, 1)
    mfrc.write_block(txt2, 2)
    mfrc.write_block(txt3, 3)

    

    
finally:
	GPIO.cleanup()

