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

I obtained the domain name thecanary.duckdns.org for free using good old [**duckdns**](duckdns.org), and dynamically bound it to the AWS server's IP address using the following [**guide**](https://www.duckdns.org/install.jsp?tab=linux-cron&domain=thecanary). This means that even if our AWS server goes down or changes IP addresses, once it comes back online the will automatically update the IP address that our domain points to, making our system more realiable.

I already had nginx installed from a previous project on this AWS instance. In order to update the configurations to point to our new domain name by changing the /etc/nginx/sites-enabled/default file, which has a copy included [**here**](nginx_default). This configuration automatically redirects any HTTP traffic to use HTTPS, and forwards these connections to our web-app frontend which runs on port 3000.

To use HTTPS, I used the Certbot ACME client to add LetsEncrypt SSL certificates for our domain and install them into nginx as per their [**instructions**](https://certbot.eff.org/instructions?ws=nginx&os=ubuntubionic). I also uninstalled the certificates that were associated with a previous project using `sudo certbot delete`

Additionally, set up the certificate to auto-renew every week as certificates are only valid for 3 months. This was done by adding the following `cron` job: `30 2 * * 1 /usr/bin/certbot renew >> /var/log/le-renew.log`, which renews the certificate every monday at 2:30am (UTC). The expiry date of a certificate can be checked with `sudo certbot cerfiticates`.

