Mosquitto broker
================
I've set up an MQTT broker on my AWS instance using [mosquitto](http://mosquitto.org/download/).

Followed the following [guide](https://obrienlabs.net/how-to-setup-your-own-mqtt-broker/) to get a mosquitto set up on my AWS instance. Have authentication (for more details, see [**users**](#users)), clients must know password in order to publish or read from particular topics, as well as websockets (not sure if this will be needed). The following commands are useful:
- `sudo service mosquitto start` to start up the MQTT broker
- `sudo mosquitto -c /etc/mosquitto/mosquitto.conf` to ensure authentication permissions are being used (I think this needs to be running to use sub / pub)
- `mosquitto_sub -h localhost -t test/#` to subscribe to the "weather" topic (example, change names and add topics as needed). The `#` means that it will listen to all subtopics under weather (only use for debugging)
- `mosquitto_pub -h localhost -t "test/test" -m "<message>"` to publish to a topic (this wont work with authentication)
- `mosquitto_pub -h localhost -t "test/test" -m "<message>" -u "<username>" -P "<password>"` to publish to a topic using authentication
- `sudo cat /var/log/mosquitto/mosquitto.log` to view logs
- `sudo nano /etc/mosquitto/acl` to edit permissions
- `sudo nano /etc/mosquitto/conf.d/myconfig.conf` to edit config

**SSL**
SSL encryption for the broker was set up as follows:
- Created my own certificate authority certificate key pair (giving the key a password): 
    `$ openssl req -new -x509 -days 1095 -extensions v3_ca -keyout ca.key -out ca.crt`
- Generated a key and certificate for mosquitto, and signed it with the CA key:
  *N.B. When asked for 'common name', put in domain name (thecanary.duckdns.org)*
```
$ openssl genrsa -out mosquitto.key 2048
$ openssl req -out mosquitto.csr -key mosquitto.key -new
$ openssl x509 -req -in mosquitto.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out mosquitto.crt -days 1095
```
- Moved the [CA certificate](cert/ca.crt) to /etc/mosquitto/ca_certificates, and the [mosquitto certificate](cert/mosquitto.crt) and [key](cert/mosquitto.key) to /etc/mosquitto/certs.
- Updated the mosquitto config file to use encrypted communication on port 8883 (and 9001 for websockets -- unused), see [**mosquitto_config**](mosquitto_config).


After rebooting the instance, the MQTTS functionality was tested as follows:
```
mosquitto_sub -h thecanary.duckdns.org -p 8883 -t "test/#" --cafile ca.crt
     
mosquitto_pub -h thecanary.duckdns.org -p 8883 -t "test/test" --cafile /etc/mosquitto/ca_certificates/ca.crt -m "<message>"
```

*SSL on pi*
- Created a key and certificate for the pi, and signed it with the CA key (identical to mosquitto)
- Set up the mqtt client as follows:
```Python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.tls_set(ca_certs='AWS/cert/ca.crt', certfile='AWS/cert/pi.crt', keyfile='AWS/cert/pi.key')
res = client.connect('thecanary.duckdns.org', port=8883)
print(f'Connect status: {mqtt.error_string(res)}')
```
- Publishes were recieved by `mosquitto_sub` client on AWS instance


Topics
-------
The following functionality is required of our MQTT communication:
- Sensor sends measurements
- Webapp specifies sampling rate

Therefore suggests the following topics:
**sensor/instructions**
Published to by web-app, subscribed to by ESP32
- `sensor/instructions/sampling` sends new sampling frequency

**sensor/data**
Published to by ESP32, subscribed to by web-app
- `sensor/data` contains sensor data

We can therefore update the publishing rights to the topics to only allow the web-app / sensor to respectively publish to those topics. Additionally these topics can only be read from our web-app / sensor to prevent outside connections from accessing them

<a name="users"></a>Users
-------------------------
I am making the following 2 users to limit access to the topics above (storing the users and passwords here cause plain text password storage is the one). I might keep them here permanently as security is more for the purposes of the assessment, it's not like anyone is actually gonna try and hijack our stuff. Obviously if I needed to be serious about security measures I wouldn't leave these here.
- sensor:2Q7!#fXb6zcaU*DY
i.e. mosquitto_pub -h localhost -t "sensor/data" -m "<message>" -u "sensor" -P "2Q7!#fXb6zcaU*DY"
- webapp:=ZCJ=4uzfZZZ#36f

These were added to the broker using [**this guide**](http://www.steves-internet-guide.com/mqtt-username-password-example/). The rights of these users were defined in the Access Control List (acl), and allows them to use **sensor/instructions** and **sensor/data** as described above.