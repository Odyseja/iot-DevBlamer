#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto
import serial
from threading import Thread


def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))


def on_message(mqttc, obj, msg):
    position = find_position(str(msg.payload))
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)
    if position:
        ser.write(chr(position))
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

developers = {"Maciek":6, "Katarzyna":22, "success":0}


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
    return developers[name]

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto() 
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

if len(sys.argv) < 6:
    print("Wrong amount of arguments: python "+sys.argv[0]+" address port")
    sys.exit(1)

turn_green_light()

broker_address = str(sys.argv[1])
broker_port = int(sys.argv[2])
my_name = str(sys.argv[3])
my_position = int(sys.argv[4])
hom_many_devs = int(sys.argv[5])

mqttc.connect(broker_address, broker_port, 60)

mqttc.subscribe("temp/blamer", 0)

mqttc.loop_forever()

 