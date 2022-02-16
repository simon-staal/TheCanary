import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected: {mqtt.error_string(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test/#")
    client.subscribe("sensor/instructions/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f'{msg.topic}: {msg.payload}')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs='AWS/cert/ca.crt', certfile='AWS/cert/pi.crt', keyfile='AWS/cert/pi.key')
client.username_pw_set('sensor', '2Q7!#fXb6zcaU*DY')

client.connect("thecanary.duckdns.org", 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()