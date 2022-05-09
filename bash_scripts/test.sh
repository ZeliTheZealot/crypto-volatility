#!/bin/sh
# Author: Benjamin
echo "Hello World!"
echo "First param: $1"
echo "Second param: $2"
for ARG in $*
do
	echo $ARG
done
