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
- I used a modified version of [**this**](https://github.com/owntracks/tools/blob/master/TLS/generate-CA.sh) script, where I specified the host to be the public IP address of the AWS instance. 
- I moved the ca.crt and IP.* files to /etc/mosquitto/certs and updated the mosquitto config file.
- Rebooted instance and tested as follows:
```
mosquitto_sub -t \# -v --cafile /etc/mosquitto/certs/ca.crt -p 8883
     
mosquitto_pub --cafile /etc/mosquitto/certs/ca.crt -h localhost -t "test/secure" -m "hello securely" -p 8883
```
- Then copied over the ca.crt file and used convert.cpp to put it into the mqtt_client.ino file for the esp32.
- MQTT client now using WiFiClientSecure instead of just WifiClient, and certificate is used to connect to the broker securely.
- On the REST API side, used updated settings to connect to the broker, but since the connection is local, unencrypted communication can also be used.

Updated broker to use encrypted communication on port 8883 with the outside world, only using port 1883 locally. MQTT client works with this.

Updated esp32 mqtt client to use encrypted port, untested (will test again at home)
Refer to this: http://www.iotsharing.com/2017/08/how-to-use-esp32-mqtts-with-mqtts-mosquitto-broker-tls-ssl.html

<a name="users"></a>Users
-------------------------
I am making the following 2 users to limit access to the topics above (storing the users and passwords here cause plain text password storage is the one). I might keep them here permanently as security is more for the purposes of the assessment, it's not like anyone is actually gonna try and hijack our stuff. Obviously if I needed to be serious about security measures I wouldn't leave these here.
- esp32:#8HAGxb3*V%+CD8^
i.e. mosquitto_pub -h localhost -t "fromESP32/test" -m "<message>" -u "esp32" -P "#8HAGxb3*V%+CD8^"
- webapp:=ZCJ=4uzfZZZ#36f

The rights of these users allows them to use **toESP32** and **fromESP32** as described above.