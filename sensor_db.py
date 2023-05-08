import RPi.GPIO as GPIO
import sys
import time
import pymysql
import smbus

address = 0x48
A0 = 0x24

bus = smbus.SMBus(1)
conn = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="sensordb")
try :
    with conn.cursor() as cur :
        sql="insert into mysql values(%s,%s,%s)" 
        while True:
            bus.write_byte(address,A0)
            value = bus.read_byte(address) #get water level sensor value
            if value is not None:
                print(value)
                #use daytime to extract latest value
                cur.execute(sql,('Water',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),value))
                conn.commit()
            else:
                print("Failed to get reading.")
            time.sleep(0.05)
except KeyboardInterrupt :
    exit()
finally :
    conn.close()
