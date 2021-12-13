import time
import drivers
from time import sleep
import RPi.GPIO as GPIO
from SimpleMFRC522 import SimpleMFRC522

tm = time.localtime()
mfrc = SimpleMFRC522()
display = drivers.Lcd()

try:    
    while True:
    
        display.lcd_display_string("Press the button", 1)  
        display.lcd_display_string("   and scan     ", 2)
        sleep(3)
        
        display.lcd_display_string("Press the button", 1)  
        display.lcd_display_string("   and scan  -->", 2)
        sleep(3)

        barcode = str(input("input barcode\n"))
        
        if (tm.tm_mday < 10):
            to_data = str(tm.tm_year) + str(tm.tm_mon) + "0" + str(tm.tm_mday)
        else:
            to_data = str(tm.tm_year) + str(tm.tm_mon) + str(tm.tm_mday)
              
        if barcode[0:8] == to_data :
            display.lcd_clear() 
            
            print(barcode[8:13])
            data = int(barcode[8:13])
            
            print(data)

            if(data < 20000) :
                display.lcd_display_string("  free parking  ", 1)
                
                if(data == 1) :              
                    dis_time = 1 
                    
                elif(data == 2) :                  
                    dis_time = 2
                    
                elif(data == 3) :                  
                    dis_time = 3 
                 
                    
            else :  
            
                display.lcd_display_string(" purchase amount", 1)  
                display.lcd_display_string("    " + str(data) + "  " , 2)
                sleep(2)
                
                display.lcd_display_string("  free parking  ", 1)
                
                if((data >= 20000) and (data < 30000) ) :
                    dis_time = 1
                    
                elif((data >= 30000) and (data < 40000) ) :
                    dis_time = 2
                    
                elif((data >= 40000) and (data < 50000) ) :
                    dis_time = 3
                
                
                display.lcd_display_string("  " + str(dis_time) + " hour ", 2)    
                                                                                              
            
                print("Now place your tag to write")
                
                id,txt_dis= mfrc.read_block(3)                           
                
                discount = int(txt_dis) + dis_time
                
                print(discount)
                
                mfrc.write_block(str(discount), 3)
                
                display.lcd_clear() 


            
finally:
	GPIO.cleanup()

