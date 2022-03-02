The Canary - Embedded Systems CW1
=============================
This repository contains all the files developed as part of ELEC60013 - Embedded Systems.

The Canary is an IoT sensor network intended to be used by miners or any other industries which require human labour in confined spaces. Sensors are all controlled by a raspberry pi which performs initial data processing, and measure:
- CO2 
- TVOC
- Temperature
- Humidity
- Air pressure

The temperature and humidity readings are used to improve the accuracy of the CO2 and TVOC readings. Data is sent to our server via MQTT over TLS, with all certificates used by our system signed by The Canary CA. Data on the server is processed and securely stored in an external database. Users can interact with this system via our web-app, which can be accessed [**here**](https://thecanary.duckdns.org), which I (sts219) will host until my EC2 free trial expires. This allows the sensor sampling rate to be specified, data to be archived, and displays metrics in a digestible format. The promotional website for the product can be found [**here**](https://kc31949.wixsite.com/the-canary).

Find a guide to the repository below:

[AWS](AWS)
-------
This folder contains the configuration files for the MQTT broker and nginx web server, instructions for the provisioning of the instance, and all the certificate/key pairs for the nodes in our system (yes I know that's not secure this is a uni project).

[backend](backend)
----------
This folder contains the files for our backend server, which processes data and handles communication between the sensors, the database and the frontend clients.

[frontend](frontend)
-----------
This folder contains the files for our web-app which the user interacts with.

[pi](pi)
-----
This folder contains the sensor interfaces and main code which runs on our pi device.

[website]
---------
https://kc31949.wixsite.com/the-canary

Contributors
------------
- Simon Staal (sts219) - System Architecture, Sensor Interfaces, Web-app
- Petra Ratkai (petraratkai) - Web-app
- Aaron Ko (TszwangKo) - Sensor Interfaces, Promotional Material
- Kai Connway-Lai (kc319) - Pi, Promotional Material
