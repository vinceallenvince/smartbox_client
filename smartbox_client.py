import RPi.GPIO as GPIO
import time
from urllib2 import Request, urlopen, URLError
import json

## TODO
# set smartbox-ch1 preset
#

GPIO.setmode(GPIO.BCM)

ready = False
base_client_uri = "http://127.0.0.1:15004"
base_server_uri = "http://162.243.120.32:8888"

###################

LED = 14
LED_count = 0
LED_state = 1
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)

def led_on():
    GPIO.output(LED, True)

def led_off():
    GPIO.output(LED, False)

###################

button_thumb_up = 23
button_thumb_down = 12

GPIO.setup(button_thumb_up, GPIO.IN, pull_up_down=GPIO.PUD_UP) #thumb up
GPIO.setup(button_thumb_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

###################

def play():
    req = Request(base_client_uri + "/action?action=play")
    urlopen(req)

def set_volume(y):
    vol = scale(y, (0.0, +20.0), (0.0, +65535.0)) + init_volume_val
    print(vol)
    if vol > 0 and vol < 65535 :
        req = Request(base_client_uri + "/action?action=volume&level=" + `vol`)
        urlopen(req)
    # if volume = 0; pause playback

def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def check_ready():
    global ready, LED_count, LED_state, Request, URLError
    if ready == False :
        req = Request(base_client_uri + "/status-data")
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, "reason"):
                LED_count += 1
                if LED_count > 40:
                    LED_state *= -1
                    LED_count = 0
                if LED_state == 1:
                    led_on()
                else:
                    led_off()
                #print 'We failed to reach a server.'
                #print 'Reason: ', e.reason
            elif hasattr(e, "code"):
                #print 'The server couldn\'t fulfill the request.'
                #print 'Error code: ', e.code
                pass
        else:
            # everything is fine
            ready = True
            led_on()
            #set_volume(5) # range is -10 -> 10
            #play()

while True:
    #if ready == True :
        input_state = GPIO.input(button_thumb_up)
        if input_state == False:
            print('Button Pressed')
            led_on()
            time.sleep(0.2)

        input_state = GPIO.input(button_thumb_down)
        if input_state == False:
            print('Button Pressed')
            led_off()
            time.sleep(0.2)

    #else:
        #check_ready()


