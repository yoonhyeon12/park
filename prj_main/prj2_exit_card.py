import serial, io, time
import RPi.GPIO as GPIO
from SimpleMFRC522 import SimpleMFRC522


ser  = serial.Serial('/dev/ttyUSB2',9600)
tm   = time.localtime()
mfrc = SimpleMFRC522()

id_now = "start"

try:    
    while True:       
    
        txt_carNo = ""
        print("--------------")
        print("Tag your card~") 
        print("--------------")        
        # wait for tagging
        id,text = mfrc.read_block(0)
        id,text_name  = mfrc.read_block(1)
        id,txt_carNo  = mfrc.read_block(2)
        id,txt_dscnt  = mfrc.read_block(3)
        
        print(txt_carNo)
        
        if id != id_now :
            id_now = id
        
            carNo = txt_carNo.split()
            dscnt = txt_dscnt.split() 
           
            #print(carNo)
            #차번호보내기
            data = str(carNo[0])
            print(data)
            data = data.encode('utf-8')
            ser.write("num".encode('utf-8'))
            ser.write(data)
            ser.write("\n".encode('utf-8'))
           
           
            #출차시간보내기
            data = str(round(time.time()))
            print(data)
            data = data.encode('utf-8')
            ser.write("tim".encode('utf-8'))
            ser.write(data)
            ser.write("\n".encode('utf-8'))           
            
            #할인금액보내기
            data = str(dscnt[0]) 
            print(data)
            data = data.encode('utf-8')
            ser.write("dis".encode('utf-8'))
            ser.write(data)
            ser.write("\n".encode('utf-8'))
            
            
            mfrc.write_block('0', 3)
        else:   pass
            
finally:
	GPIO.cleanup()
      