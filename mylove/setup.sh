#!/usr/bin/env bash

ROOTID="0"

if [ "$(id -u)" -ne $ROOTID ]; then
	echo "This script must be executed with root privileges"
	exit 1
fi

echo "Installing...\m/\n"

pip install urllib2 2> /dev/null
pip install bs4 2> /dev/null
pip install prettytable 2> /dev/null
