#!/usr/bin/env bash

# build.sh - a front-end to ./bin/carrel2json.py and ./bin/template2html.sh

# Eric Lease Morgan <emorgan@nd.edu>
# August 7, 2019 - first documentation


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
