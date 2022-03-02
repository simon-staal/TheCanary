#!/bin/bash

set -euo pipefail

IP="35.178.173.40"

#if [[ $# -eq 0 ]] ; then
#    >&2 echo "Usage: ./halt_server.sh <IP>"
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

  if screen -list | grep -q "mosquitto"; then
    echo "Halting MQTT broker"
    screen -X -S "mqtt" quit
    echo "$SEP"
  fi
  
  echo "$SEP"
  echo "Attempting graceful shutdown of REST web service"
  sudo kill $(ps h --ppid $(screen -ls | grep rest | cut -d. -f1) -o pid)
  echo "Shut down REST web service successfully (and gracefully ;D)"
  echo "$SEP"

  echo "Attempting graceful shutdown of REACT web-app"
  sudo kill $(ps h --ppid $(screen -ls | grep react | cut -d. -f1) -o pid)
  echo "Shut down REACT web-app successfully"
  echo "$SEP"

  echo "Server processes halted, Done"
EOF
