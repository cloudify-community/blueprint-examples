#!/bin/bash

#get the port number from node's properties
port = `ctx node properties port`
#create a temporary directory for the server
cd `mktemp -d`

#Crate the Hello World message in index.html
echo "WeServer root" > index.html

#Run the wenserver process in background on the port cpesified and save process id to a pid.txt
env -i /bin/bash -c "nohup python3 -m http.server $port > server_log.txt 2>&1 & echo \$! > pid.txt"

#update the node instance with the process id from the pid.txt file so it can be tracked later
ctx instance runtime-properties pid `cat pid.txt`
#update the node instance with tmp path
ctx instance runtime-properties path `pwd`
