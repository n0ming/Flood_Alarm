import re
import sys
import cv2
import pymysql
import time
import numpy as np
from level1_buzzer import buzzer
from level3_msg import e_msg

#people detection
detection_count1 = 0
detection_count2 = 0

#camera setting
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(cv2.CAP_V4L2)
count_array = np.zeros(100,dtype=int)
while True :
    num_disposable = 0

    #DB setting
    conn = pymysql.connect(host="localhost",
                       user="root",
                       passwd="root",
                       db="sensordb")
    cur = conn.cursor()
    #extract latest data values
    cur.execute('select value from mysql where (value, daytime) in (select value, max(daytime) from mysql group by value)')
    raw_datas = cur.fetchall()
    #extract only water value from DB excluding special symbols
    data = re.findall("'([^']*)'",str(raw_datas)) 
    list_a = list(map(int,data))
    my_array = np.array(list_a)
    
    #convert from string to integer 
    for i in range(len(my_array)):
        x = int(my_array[i])

    #Run By Water Level        
    #water level1
    print(x)
    if(20<x and x<=165):
        print("water value : %s"%x)
        print("      level 1")
        #warning
        buzzer()
	
    #water level2
    elif(172<=x and x<192): #connect family function
        print("water value : %s"%x)
        print("      level 2")
        #people detection using camera
        ret, frame = cap.read()
        frame1 = cv2.resize(frame,dsize=(640, 480))
        font = cv2.FONT_HERSHEY_SIMPLEX
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        boxes, weights = hog.detectMultiScale(frame1, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
		#display the detected boxes in the colour picture
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(frame1, (xA, yA), (xB, yB),(0, 255, 0), 2)
            detection_count1+=1
        cv2.putText(frame1, "peoplecount: " + str(detection_count1), (20, 50), 0, 2, (255, 0, 0), 3)
		
        img = cv2.resize(frame1,(640,480))
        #cv2.imshow("Frame", frame1) #Commented out because an error occurred in the remote terminal.
        key = cv2.waitKey(1) & 0xFF
        print ("cumulative detection count" ,detection_count1)
		
    #water level3
    elif(x>=192): 
        print("water value : %s"%x)
        print("      level 3")
        print(x)

        #people detection using camera
        ret, frame = cap.read()
        frame1 = cv2.resize(frame,dsize=(640, 480))
        font = cv2.FONT_HERSHEY_SIMPLEX
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        boxes, weights = hog.detectMultiScale(frame1, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
		#display the detected boxes in the colour picture
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(frame1, (xA, yA), (xB, yB),(0, 255, 0), 2)
            detection_count2+=1
        cv2.putText(frame1, "peoplecount: " + str(detection_count2), (20, 50), 0, 2, (255, 0, 0), 3)
		
        img = cv2.resize(frame1,(640,480))
        #cv2.imshow("Frame", frame1)
        key = cv2.waitKey(1) & 0xFF
        print ("cumulative detection count" ,detection_count2)
		
        #trun off camera if water level is 0
        if x==0:
            cap.release()
            cv2.destroyAllWindows()
			
        #send emergency message
        if detection_count1>0 & detection_count2>0 : 
            #Since a person was recognized at water level 2, a message is sent even if a person is recognized at water level 3
            if num_disposable == 1:
                print("msg")
                e_msg()
                num_disposable = 0
        elif detection_count1==0 & detection_count2>2 :
            #Since a person was not recognized at water level 2, it is unlikely to be recognized as a person at level 3, so the count value standard is raised to prevent errors.
            if num_disposable == 1:
                print("msg")
                e_msg()
                num_disposable = 0
