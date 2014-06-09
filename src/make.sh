#! /bin/sh

if [ "$1" = "clean" ]; then
	find -name '*.pyc' -exec rm {} \;
else
	echo 'Usage: ./make.sh clean'
fi
