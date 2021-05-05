#!/bin/bash
if [ "$2" == "0" ]
then
	kill -s SIGTERM "$1"
else
	kill -s SIGKILL "$1"
fi