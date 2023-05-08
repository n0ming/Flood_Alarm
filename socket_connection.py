import socket
import pymysql
import re
import sys
import cv2
import time
import numpy as np
LOCALHOST = "172.30.1.69" #raspberry pi address
PORT = 8110  #random port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST,PORT))
server.listen(1)
send_warn=""
send_method="lf you want to know about water level of your house, please enter this sentense,'Water Level'!"
while True:  #wait for Android to press connect button
    client_sock, addr = server.accept() #connection approval

    if client_sock: #If client_sock is not null (connection accepted)
        print('Connected by?!', addr) 
        client_sock.send(str(send_method).encode("utf-8"))
        while True:
            conn = pymysql.connect(host="localhost",
                                   user="root",
                                   passwd="root",
                                   db="sensordb")
            cur = conn.cursor()
            cur.execute('select value from mysql where (value, daytime) in ( select value, max(daytime) as daytime from mysql group by value)')
            raw_datas = cur.fetchall()
            #extract only water value from DB
            data = re.findall("'([^']*)'",str(raw_datas))
            list_a = list(map(int,data))
            my_array = np.array(list_a)
            for i in range(len(my_array)):
                x = int(my_array[i])
            in_data = client_sock.recv(1024)
            print('rcv :', in_data.decode("utf-8"), len(in_data)) #전송 받은값 디코딩
            if in_data.decode("utf-8")=='Water Level':
                if(x<20):
                    send_warn = "...."
                if(20<=x and x<=150):
                    send_warn = ("level 1 | value : %s"%x) #%s to check getting the latest db value in real time
                elif(160<=x and x<195):
                    send_warn = "level 2" 
                elif(x>=196):       
                    send_warn = ("level 3%d"%x)
                client_sock.send(str(send_warn).encode("utf-8"))  #transmit int value encoded as string
                print('Respond : ', send_warn)
