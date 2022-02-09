import paho.mqtt.client as mqtt
from time import sleep

client = mqtt.Client()
############################################
def on_message(client, userdata, message) :
    print("Message received")
    print("Received message:{} on topic {}".format(str(message.payload.decode("utf-8")), message.topic))
############################################

#Setting keys for encripted connection
client.tls_set(ca_certs="mosquitto.org.crt",\
                certfile="client.crt",\
                keyfile="client.key")

#Attach callback function
client.on_message=on_message

returnCode = client.connect("test.mosquitto.org",port=8884)
print("...")
print(f"connect status: {mqtt.error_string(returnCode)}\n")

sleep(2)

print("Subscribing to topic","IC.embedded/TeamEpicGamers/#")
client.subscribe("IC.embedded/TeamEpicGamers/test")

for i in range(1,1000):
    client.loop_start() #start the loop

    print(f"Waiting for message: time {i*10}")

    sleep(10) # wait
    client.loop_stop() #stop the loop
