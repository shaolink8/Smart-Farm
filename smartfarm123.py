import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import smtplib
import httplib, urllib
key='PIRHDCZ6Y75LLAHW'
camera = PiCamera()
camera.start_preview()
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 22
GPIO_ECHO = 21
GPIO_ECHO2=20
GPIO_ECHO3=12
GPIO_ECHO4=16
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_ECHO2,GPIO.IN)
GPIO.setup(GPIO_ECHO3,GPIO.IN)
GPIO.setup(GPIO_ECHO4,GPIO.IN)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(13,GPIO.IN)
GPIO.setup(8,GPIO.IN)
GPIO.setup(7,GPIO.OUT)
GPIO.output(26,GPIO.LOW)
time.sleep(4)
totaltime=0
stime=0
ttime=0
while True:
    def distance():        
        GPIO.output(26, True)
        time.sleep(0.00001)
        GPIO.output(26, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        return distance
    def distance2():   
        GPIO.output(26, True)
        time.sleep(0.00001)
        GPIO.output(26, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO2) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO2) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance2 = (TimeElapsed * 34300) / 2
        return distance2
    def distance3():
         GPIO.output(26, True)
         time.sleep(0.00001)
         GPIO.output(26, False)
         StartTime = time.time()
         StopTime = time.time()
         while GPIO.input(GPIO_ECHO3) == 0:
             StartTime = time.time()
         while GPIO.input(GPIO_ECHO3) == 1:
             StopTime = time.time()
         TimeElapsed = StopTime - StartTime
         distance3 = (TimeElapsed * 34300) / 2
         return distance3
    def distance4():
        GPIO.output(26, True)
        time.sleep(0.00001)
        GPIO.output(26, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO4) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO4) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance4 = (TimeElapsed * 34300) / 2
        return distance4
    def smokesensor():
        print("Activate to proceed")
        if GPIO.input(13):
            t=GPIO.input(13)
            print("Smoke Detected")
            GPIO.output(26,GPIO.HIGH)
            time.sleep(0.5)
            params = urllib.urlencode({'field5': t,'key':key }) 
            headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = httplib.HTTPConnection("api.thingspeak.com:80")
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()
            conn.close()
            time.sleep(0.5)
        else:
            GPIO.output(26,GPIO.LOW)
    def moisturesensor():
        if GPIO.input(8)==0:
            print("Moisture enough")
        else:
            GPIO.output(7,GPIO.HIGH)
    if __name__ == '__main__':
        try:
            while True:
                smokesensor()
                dist1 = distance()
                dist2=distance2()
                dist3=distance3()
                dist4=distance4()
                moisturesensor()
                if(dist1<15 or dist2<15 or dist3<15 or dist4<15):
                    GPIO.output(26,GPIO.HIGH)
                elif(dist1>15 and dist2>15 and dist3>15 and dist4>15):
                    GPIO.output(26,GPIO.LOW)
                print ("Measured Distance 1 = %.1f cm" % dist1)
                print ("Measured Distance 2 = %.1f cm" % dist2)
                print ("Measured Distance 3 = %.1f cm" % dist3)
                print ("Measured Distance 4 = %.1f cm" % dist4)
                params = urllib.urlencode({'field1': dist1, 'field2': dist2,'field3':dist3,'field4':dist4,'key':key }) 
                headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                conn = httplib.HTTPConnection("api.thingspeak.com:80")
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print response.status, response.reason
                data = response.read()
                conn.close()
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
    


    
    
 



    
    
