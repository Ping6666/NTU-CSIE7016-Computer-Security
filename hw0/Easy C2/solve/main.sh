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

# --- init server --- #

port=11187

nc -kl $port&
_wait_port $port

nc_pid=$!
trap "_sigint $nc_pid" SIGINT

# --- run easy-c2 --- #

../src/easy-c2

# --- wait the pid --- #

wait $nc_pid
