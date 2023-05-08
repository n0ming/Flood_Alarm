import socket
import pymysql
import re
import sys
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
import smbus

LOCALHOST = "172.30.1.69" #raspberry pi address
PORT = 8097 #random port
conn = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db="sensordb")

# DB setting
cur = conn.cursor()
cur.execute('select value from collect_data where (value, daytime) in ( select value, max(daytime) as daytime from collect_data group by value)')
raw_datas = cur.fetchall()

# extract only water value from DB
data = re.findall("'([^']*)'",str(raw_datas)) 
list_a = list(map(int,data))
my_array = np.array(list_a)
for i in range(len(my_array)):
    x = int(my_array[i])

send_warn=""
send_method="If you want to know about water level of your house, please enter this sentence, 'Water Level'!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen(1)

address = 0x48
A0 = 0x24
bus = smbus.SMBus(1)

try:
    with conn.cursor() as cur:
        sql = "insert into collect_data values(%s,%s,%s)"
        while True:
            bus.write_byte(address, A0)
            value = bus.read_byte(address) #data value received from water level detection sensor
            if value is not None:
                print(value) #check the data value
                cur.execute(sql, ('Water', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), value))
                conn.commit()
            else:
                print("Failed to get reading.")
            time.sleep(0.05)

            client_sock, addr = server.accept() #connection approval

            if client_sock: #If client_sock is not null (connection accepted)
                print('Connected by?!', addr) 
                client_sock.send(str(send_method).encode("utf-8"))
                while True:
                    in_data = client_sock.recv(1024)
                    print('rcv :', in_data.decode("utf-8"), len(in_data)) #decoding the received value
                    if in_data.decode("utf-8") == 'Water Level':
                        if 0 < x and x < 165: #Leave empty by 5 for margin of error
                            send_warn = "level 1"
                        elif 172 <= x and x < 192:
                            send_warn = "level 2" 
                        elif x >= 192 :       
                            send_warn = "level 3"
                        client_sock.send(str(send_warn).encode("utf-8")) # transmit int value encoded as string
                        print('Respond : ', send_warn)
except KeyboardInterrupt:
    exit()
finally:
    conn.close()
