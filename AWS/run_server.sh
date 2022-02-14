#!/bin/bash

set -euo pipefail

IP="3.8.182.14"

# if [[ $# -eq 0 ]] ; then
#    >&2 echo "Usage: ./run_server.sh <IP>"
#    >&2 echo "<IP> is the IP of the instance being connected to"
#    exit 1
#fi

# Finds ssh key
KEY=$(echo *.pem)
echo "${KEY}"

# Error checking
if [[ -z "${KEY}" ]] ; then
  >&2 echo "Error: No ssh permission file could be found in directory"
  >&2 echo "       Please include the permission file to ssh into the desired instance"
  exit 1
fi

WS=" "
if [[ ${KEY} =~ $WS ]]; then
  >&2 echo "Error: Multiple ssh permission files found in directory"
  >&2 echo "       Please have only 1 permission file for the desired instance"
  exit 1
fi

# Formatting
TERMINAL_WIDTH=$(tput cols)
SEP=$(echo $(printf '=%.0s' $(eval "echo {1.."$(($TERMINAL_WIDTH))"}")))

echo "$SEP"
echo "Connecting to server instance"
ssh -A -i ${KEY} ubuntu@${IP} << EOF
  #!/bin/bash
  set -euo pipefail
  echo "Connection successful"
  echo "$SEP"
  #echo "Installing packages"
  #sudo apt update
  #sudo apt -y install nodejs
  #echo "Packages installed successfully"
  #echo "$SEP"
  echo "Building project"
  if [[ -d "Y2_Project" ]]; then
    cd Y2_Project
    git pull origin master
    cd
  else
    git clone git@github.com:sts219/Y2_Project.git
  fi
  echo "Most recent version obtained"

  echo "$SEP"
  if sudo lsof -i -P -n | grep -q mosquitto
  then
    echo "mosquitto MQTT broker running";
  else
    echo "Launching mosquitto MQTT broker"
    screen -d -m -S mqtt bash -c 'sudo mosquitto -c /etc/mosquitto/mosquitto.conf'
  fi
  echo "$SEP"

  echo "$SEP"
  if sudo lsof -i -P -n | grep -q nginx
  then
    echo "nginx web server running"
  else
    echo "Launching nginx web server"
    sudo systemctl start nginx
  fi
  echo "$SEP"

  echo "$SEP"
  echo "Launching REST web service"
  screen -d -m -S rest bash -c 'cd ~/Y2_Project/Server && npm start'
  echo "$SEP"

  echo "Launching REACT web app"
  screen -d -m -S react bash -c 'cd ~/Y2_Project/Front_End/React/web-app && npm start'
  echo "$SEP"
  
  echo "Server running, Done"
EOF
