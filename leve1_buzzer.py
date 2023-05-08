import RPi.GPIO as GPIO
import time

def buzzer():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    buzzer  = 23
    scale = 261   #buzzer sound value
    
    GPIO.setup(buzzer, GPIO.OUT)             
    p = GPIO.PWM(buzzer, 100)
    
    try:                        
        p.start(100)                            
        p.ChangeDutyCycle(90)                      
        p.ChangeFrequency(scale) 
        time.sleep(0.05)
        p.stop()                           

    except KeyboardInterrupt:                      
        GPIO.cleanup()
