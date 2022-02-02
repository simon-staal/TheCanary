Embedded Systems Coursework 1
=============================
Use this file to keep track of shit.

Pi Setup
--------
- Follow [**setup lab instructions**](lab-instructions-cw1-part1.pdf), you can skip the part about researching the sensor, make sure I2C / python is installed
- Install git:
  ```
  $ sudo apt update
  $ sudo apt install git
  ```
- Add an ssh key for your raspberry pi as follows:
  ```
  $ ssh-keygen -t ed25519 -C "<your_github_email>"
  // Press enter through all the prompts
  $ cat ~/.ssh/id_ed25519.pub 
  ```
  Copy the output to your clipboard and paste it into the relevant field to add a new key here.

  You should now be able to clone the repo onto your raspberry pi

CCS811 Air Quality Sensor
-------------------------
Datasheet: https://cdn.sparkfun.com/assets/2/c/c/6/5/CN04-2019_attachment_CCS811_Datasheet_v1-06.pdf

Wiring: https://blog.adafruit.com/2017/08/14/updated-guide-adafruit-ccs811-air-quality-sensor-with-raspberry-pi-wiring-instructions-and-python-code-adafruitlearningsystem/

Guide: https://www.avimesa.com/docs/dev-kits/kit-5-air-quality-using-a-raspberry-pi/

Adafruit MPRLS Air Pressure Sensor
-------------------------
Company Website: https://www.adafruit.com/product/3965

Si7021-A20 HUMIDITY AND TEMPERATURE SENSOR
-------------------------
DataSheet: https://cdn-learn.adafruit.com/assets/assets/000/035/931/original/Support_Documents_TechnicalDocs_Si7021-A20.pdf
