##PingFunction
##Version 0.1
##Codey Sivley
import subprocess
import time
import re
import RPi.GPIO as GPIO
import datetime
## declare the only constant
hostname = "8.8.8.8" #google's dns server
## declare functions. veryfast(), fast(), medium(), and slow()
## contain the commands to trigger the LEDs
def blink(pin):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(.5)
    return
def veryfast():
    GPIO.output(12, GPIO.HIGH)
    time.sleep(.13)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(.13)
    GPIO.output(15, GPIO.HIGH)
    time.sleep(.13)
    GPIO.output(16, GPIO.HIGH)
    time.sleep(.13)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    time.sleep(.5)
    return
def fast():
    GPIO.output(12, GPIO.HIGH)
    time.sleep(.13)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(.13)
    GPIO.output(15, GPIO.HIGH)
    time.sleep(.13)
    #GPIO.output(16, GPIO.HIGH)
    #time.sleep(.13)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    #GPIO.output(16, GPIO.LOW)
    time.sleep(.5)
    return
def medium():
    GPIO.output(12, GPIO.HIGH)
    time.sleep(.13)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(.13)
    #GPIO.output(15, GPIO.HIGH)
    #time.sleep(.13)
    #GPIO.output(16, GPIO.HIGH)
    #time.sleep(.13)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    #GPIO.output(15, GPIO.LOW)
    #GPIO.output(16, GPIO.LOW)
    time.sleep(.5)
    return
def slow():
    GPIO.output(12, GPIO.HIGH)
    time.sleep(.13)
##    GPIO.output(13, GPIO.HIGH)
##    time.sleep(.13)
##    GPIO.output(15, GPIO.HIGH)
##    time.sleep(.13)
##    GPIO.output(16, GPIO.HIGH)
##    time.sleep(.13)
    time.sleep(1)
    GPIO.output(12, GPIO.LOW)
##    GPIO.output(13, GPIO.LOW)
##    GPIO.output(15, GPIO.LOW)
##    GPIO.output(16, GPIO.LOW)
    time.sleep(.5)
    return
GPIO.setmode(GPIO.BOARD)
## setup GPIO channels
GPIO.setup(11, GPIO.OUT) #RED
GPIO.setup(12, GPIO.OUT) #YELLOW LOWER
GPIO.setup(13, GPIO.OUT) #YELLOW HIGHER
GPIO.setup(15, GPIO.OUT) #GREEN LOWER
GPIO.setup(16, GPIO.OUT) #GREEN HIGHER

def main():
    # pingout() runs the OS ping command and returns it to Python.
    # some changes had to be made to work with both iOS and linux.
    # notably the error messages and regex functions.
    def pingout():
        i = (datetime.datetime.now())
        date = (i.month, i.day, i.year)
        my_file = open(str(date), "a")
        ping_process = subprocess.Popen(["ping", "-c", "1", hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        pingp = str(ping_process.stdout.read())
        print(pingp)

        if re.search(r'100.0% packet loss|100% packet loss', pingp) != None:
            print ("It's down!")
            blink(11) #RED
            with open(str(date), "a") as textfile:
                my_file.write(str(time.strftime('%X') + ",1000\n")) #default ping timeout == 1000
            time.sleep(2)
        elif re.search(r'Network is unreachable', pingp) != None:
            print ("No network")
            blink(11) #RED
            with open(str(date), "a") as textfile:
                my_file.write(str(time.strftime('%X') + ",1000\n")) #default ping timeout == 1000
            time.sleep(2)
        elif re.search(r'100.0% packet loss|100% packet loss|Network is unreachable', pingp) == None: 
            m = re.search(r'\/\d{2,4}\.\d{3}\/', pingp)
            product = m.group(0)
            #print(product)
            newproduct = product.replace('/', '')
            print(newproduct)
            #return newproduct
        
            rawvalue = newproduct
            value = float(rawvalue)
            ## THE FOLLOWING COMMENTED OUT BLINK() COMMANDS ARE OLD AND UNUSED
            ## THEY REMAIN AS VISUAL REMINDER OF PINOUT AND FOR DEBUGGING
            if value >= 100:
                print("Ping is slow")
                slow()
##                blink(12) #YELLOW
            elif value >= 50 and value < 100:
                print("Ping is medium")
                medium()
##                blink(12) #YELLOW
##                blink(13) #YELLOW
            elif value >= 25 and value < 50:
                print("Ping is fast")
                fast()
##                blink(12) #YELLOW
##                blink(13) #YELLOW
##                blink(15) #GREEN
            elif value < 25:
                print("Ping is really fast")
                veryfast()
##                blink(12) #YELLOW
##                blink(13) #YELLOW
##                blink(15) #GREEN
##                blink(16) #GREEN
            else:
                print("Error in value")
            with open(str(date), "a") as textfile:
                my_file.write(str(time.strftime('%X') + "," + rawvalue + "\n"))
            time.sleep(1.5)
        else:
            print("Error in pingout")
    now = datetime.datetime.now()
    now_time = now.time()
    while True == True:
        i = (datetime.datetime.now())
        date = (i.month, i.day, i.year)
        #my_file = open(str(date), "w+")
        now = datetime.datetime.now()
        now_time = now.time()
        if now_time >= datetime.time(8,30) and now_time <= datetime.time(18,30):
            print("yes, within the interval")
            pingout()
##        else:
##           if my_file.closed == False:
##                my_file.close()
main()

