#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto
import serial
from threading import Thread

current_position = 0


def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))


def on_message(mqttc, obj, msg):
    position = find_position(str(msg.payload))
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    if position:
        ser.write(chr(position))
    global curr
    curr=developers[str(msg.payload)]
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def turn_green_light():
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    ser.write(chr(64+8+4))


def turn_red_light():
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    ser.write(chr(64+32+16))


def turn_blue_light():
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    ser.write(chr(64+2+1))



def find_position(name):
    if name == "success":
        turn_green_light()
        return None
    elif name == my_name:
        turn_red_light()
        return None
    else:
        turn_blue_light()
    return count_num(name)

def count_num(name):
    print name
    num = developers[name]
    if (developers[my_name]+1)%3 == num: # left
        res = 25
    else:
        res = 5
    return res


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

developers = {"Passarinho": 1, "Wegrzyns":2, "Odyseja":3}

curr = 0
curr_position = 15


if len(sys.argv) < 5:
    print("Wrong amount of arguments: python "+sys.argv[0]+" address port name")
    sys.exit(1)

turn_green_light()
ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
ser.write(chr(15))

broker_address = str(sys.argv[1])
broker_port = int(sys.argv[2])
my_name = str(sys.argv[3])

mqttc.connect(broker_address, broker_port, 60)

mqttc.subscribe("temp/blamer", 0)

mqttc.loop_forever()


