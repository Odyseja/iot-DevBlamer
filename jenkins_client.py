#!/usr/bin/python

# This shows a simple example of an MQTT subscriber.

import sys
import mosquitto


def on_connect(mqttc, obj, rc):
    print("rc: "+str(rc))


def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))


def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

if len(sys.argv)<4:
    print("Wrong amount of arguments: python "+sys.argv[0]+" address port dev_to_blame")
    sys.exit(1)

broker_address = str(sys.argv[1])
broker_port = int(sys.argv[2])
dev_to_blame = str(sys.argv[3])

mqttc.connect(broker_address, broker_port, 60)
# mqttc.connect("192.168.17.40", 1883, 60)

# publishing message on topic with QoS 0 and the message is not Retained
mqttc.publish("temp/blamer", dev_to_blame, 0, False)


