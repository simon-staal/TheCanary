Server Breakdown
================
This folder documents the services running on our AWS instance, as well copies of the relevant configuarion files. We use an EC2 AWS instance to simultaniously run the following:
- Mosquitto MQTT broker
- REST API (backend)
- REACT web-app (frontend)
- nginx web server
Please find a more detailed explaination of each below:

Mosquitto MQTT broker
---------------------
This is a broker that is custom set-up to fit our needs. For more information about the broker, check [**here**](MQTT.md). When setting up the server, the following command needs to be run to start up the broker:
        `sudo mosquitto -c /etc/mosquitto/mosquitto.conf`

REST API
--------
This is a node.js app which handles requests from the REACT front-end and communicates to our pi via the MQTT broker, implemented [**here**](../backend). <del>It listens for requests on port 8080 (potentially update the instance details to ban outside connection to this port). To boot it up, simply run `npm start` in this directory.</del> Updated the REST API to use HTTPS to ensure that front-to-back communication is fully encrypted. Can also listen using HTTP on port 8080, but this option is currently disabled, only allowing https connection on port 8443 @ https://debonair.duckdns.org:8443. The backend uses the same certificates that were set up using LetsEncrypt for our nginx web server.

REACT Web-App
-------------
This is our front-end application contained [**here**](../frontend). It is hosted on port 3000, and communicates with the pi via requests to the REST API. After issues in a previous project with running react apps, I kept npm on npm@7.5.4 (as per [**this issue**](https://github.com/facebook/create-react-app/issues/10811)).

nginx Web Server
----------------
I set up an nginx web server on our AWS instance to allow us to use HTTPS on our website and forward connection requests to thecanary.duckdns.org to our REACT web app, giving us a proper domain name for browser clients to interact with our device.

To use HTTPS, I used the Certbot ACME client to add LetsEncrypt SSL certificates for our domain and install them into nginx as per their [**instructions**](https://certbot.eff.org/instructions?ws=nginx&os=ubuntubionic). I also uninstalled the certificates that were associated with a previous project using `sudo certbot delete`

Additionally, set up the certificate to auto-renew every week as certificates are only valid for 3 months. This was done 

Fixed HTTPS issues, so now have full front-to-back encryption!


Dynamic DNS setup: https://www.duckdns.org/install.jsp?tab=linux-cron&domain=thecanary

