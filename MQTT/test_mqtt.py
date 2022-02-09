import paho.mqtt.client as mqtt
from time import sleep

client = mqtt.Client()

client.tls_set(ca_certs="mosquitto.org.crt",\
                certfile="client.crt",\
                keyfile="client.key")

returnCode = client.connect("test.mosquitto.org",port=8884)
print("...")
print(f"connect status: {mqtt.error_string(returnCode)}\n")
sleep(2)
MsgInfo = client.publish("IC.embedded/TeamEpicGamers/test","hello")
print("...")
print(f"publish status: {mqtt.error_string(MsgInfo.rc)}")

for i in range(1,1000):
    client.loop_start() #start the loop

    print("Publishing message to topic","IC.embedded/TeamEpicGamers/test")
    client.publish("IC.embedded/TeamEpicGamers/test","HELLO")

    sleep(10) # wait
    client.loop_stop() #stop the loop
