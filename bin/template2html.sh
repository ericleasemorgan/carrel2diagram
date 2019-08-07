#!/usr/bin/env bash

# configure
TEMPLATE='./etc/template.htm'

# sanity check
if [[ -z $1 ]]; then
	echo "Usage: $0 <carrel>" >&2
	exit
fi

# get input
CARREL=$1

# do the work, output, and done
HTML=$( cat $TEMPLATE | sed "s/##CARREL##/$CARREL/g" )
echo $HTML
