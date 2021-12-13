import serial, io, time
from selenium import webdriver

drv = webdriver.Chrome(executable_path="/home/pi/chromedriver")

# from Entrance Card-Reder
s0 = serial.serial_for_url('/dev/ttyUSB0', 9600, timeout=1)
sio0 = io.TextIOWrapper(io.BufferedRWPair(s0, s0))

# from Exit Card-Reder
s1 = serial.serial_for_url('/dev/ttyUSB1', 9600, timeout=1)
sio1 = io.TextIOWrapper(io.BufferedRWPair(s1, s1))


if __name__ == '__main__':
    drv.get('http://localhost:8000')

    park        = {}
    carnum_out  = ""
    time_out    = 0
    time_total  = 0
    dis_tim       = 0
    carnum_in   = ""

    try:

        while True:
        
            drv.execute_script("from_py(1)")
            
            rcv0 = sio0.readline()  # recieve from entrance
            rcv1 = sio1.readline()  # recieve from 'prj_exit_card.py'


            if(rcv0 != ''):
                if(rcv0[0:3] == "num"): 
                    carnum_in = rcv0[3:7]
                    print(carnum_in)           
                elif (rcv0[0:3] == "tim"):
                    park[carnum_in] = int(rcv0[3:])
                    print(park)
                    
                    #change page
                    drv.execute_script("from_py(2)")
                    
                    #car number
                    car = int(carnum_in)
                    drv.execute_script("from_py_carnum(%d)" %(car))
                    
                    #time  
                    min_ = (park[carnum_in] // 60)%60 
                    hour = ((park[carnum_in] // 60)//60) % 24

                    drv.execute_script("from_py_time_in(%d, %d)" %(hour+9,min_))
                    time.sleep(2)
                         

            if(rcv1 != ''):
                if  (rcv1[0:3] == "num"):  
                    carnum_out = rcv1[3:7]
                    print(carnum_out)
                elif(rcv1[0:3] == "tim"):
                    time_out  = int(rcv1[3:])
                    print(time_out)
                elif(rcv1[0:3] == "dis"):
                    dis_tim = int(rcv1[3:])
                    print(dis_tim)
             
                    #주차요금계산
                    exit_time = time_out
                   
                    print(time_out)
                    print(park)
                                  
                    ent_time  = park[carnum_out]
                    
                    #parking_tm_min = (exit_time - ent_time) // 60 
                    
                    parking_tm_min = 190   
                    
                    if  parking_tm_min <= 30 :
                        charge = 0
                    elif parking_tm_min > 30 :
                        charge = (parking_tm_min - 30) * 30
                
                    
                    tim_total = parking_tm_min - (dis_tim * 60)
                    
                    if tim_total <= 30 :
                        total = 0
                    elif tim_total > 30 :
                        total = (tim_total - 30) * 30
                                                                           
                    if(total < 10) :
                        total = 0

                    #lcd 출력
                    print("차번호 : " + carnum_out)  

                    del park[carnum_out]
                    
                    print("=================")
                    #주차요금,할인금액 띄우기   
                    print(charge)
                    print(str(dis_tim) + " 시간 할인")
                    print(total)
                    print("=================")
                    
                    
                    #change page
                    drv.execute_script("from_py(3)")
                    
                    #car number
                    car = int(carnum_out)
                    drv.execute_script("from_py_carnum(%d)" %(car))
                    
                    #parking time
                    if parking_tm_min >=60 :
                        parking_hour = parking_tm_min // 60
                        parking_min  = parking_tm_min % 60
                    else:
                        parking_hour = 0
                        parking_min  = parking_tm_min
                   
                    drv.execute_script("from_py_time_total(%d, %d)" %(parking_hour,parking_min))
                    
                    #free time
                    free_tm = int(dis_tim)
                    print(dis_tim)
                    drv.execute_script("from_py_time_free(%d)" %(free_tm))
                    
                    #charge
                    drv.execute_script("from_py_charge(%d)" %(total))
                    time.sleep(2)
                    

            
    except KeyboardInterrupt:
        sio0.flush()
        GPIO.cleanup()
