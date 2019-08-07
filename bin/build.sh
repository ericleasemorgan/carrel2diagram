#!/usr/bin/env bash

# configure
CARREL2JSON='./bin/carrel2json.py'
HTML='./html'
JSON='./html/json'
TEMPLATE2HTML='./bin/template2html.sh'

# sanity check
if [[ -z $1 ]]; then
	echo "Usage: $0 <carrel>" >&2
	exit
fi

# get input 
CARREL=$1

# do the work and done
$CARREL2JSON   $CARREL > "$JSON/$CARREL.json"
$TEMPLATE2HTML $CARREL > "$HTML/$CARREL.html"
exit
