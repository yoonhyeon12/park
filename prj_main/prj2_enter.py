import RPi.GPIO as GPIO
import time
from serial import Serial
from SimpleMFRC522 import SimpleMFRC522


ser  = Serial('/dev/ttyUSB0',9600)
tm   = time.localtime()
mfrc = SimpleMFRC522()
bar  = "---"

UID = {}
id_now = "start"

try:   
   
    while True :
    
        print("--------------")
        print("Tag your card~") 
        print("--------------")
        
        
        id,text_name  = mfrc.read_block(1)
        id,text_carNo = mfrc.read_block(2)
        id,text_dscnt = mfrc.read_block(3)
        print(text_dscnt)
        
        if id != id_now :
            id_now = id
        
            name_  = text_name.split(' ')
            carNo = text_carNo.split()
       
            name = (name_[0] + " " + name_[1] + " " + name_[2] + " " + name_[3] )
            
            data = str(carNo[0])
            print(data)
            data = data.encode('utf-8')
            ser.write("num".encode('utf-8'))
            ser.write(data)
            ser.write("\n".encode('utf-8'))
                
            data = str(int(time.time()))
            print(data)
            data = data.encode('utf-8')
            ser.write("tim".encode('utf-8'))
            ser.write(data)
            ser.write("\n".encode('utf-8'))
            
            
            UID[carNo[0]] = [name]
            print(bar)
            print(UID)
            print(bar)
     
            id,text = mfrc.read_block(1);
            id,text = mfrc.read_block(2);
            
            print("year:", tm.tm_year)
            print("month:", tm.tm_mon)
            print("day:", tm.tm_mday)
            print("hour:", tm.tm_hour)
            print("minute:", tm.tm_min)
            print("second:", tm.tm_sec)
    
finally:
	GPIO.cleanup()
      
