#!/usr/bin/env python

# carrel2json.py - given the short name of a Distant Reader study carrel, output a JSON file denoting relationships between parts-of-speech

# configure
PUNCTUATION = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
POS         = 'NN'
CARRELS     = './etc/carrels'
WEIGHT      = 0

# require
from itertools import combinations
import glob
import json
import numpy as np
import os
import pandas as pd
import sys

# sanity check
if len( sys.argv ) != 2 :
	sys.stderr.write( 'Usage: ' + sys.argv[ 0 ] + " <name>\n" )
	quit()

# get input
corpus = sys.argv[ 1 ]

# define
def remove_puncutation( word ) :
	for p in PUNCTUATION :
		if p in word : return ''
	return word

# check for study carrel
if not os.path.exists( CARRELS + '/%s' % corpus):
	os.system( "mkdir -p " + CARRELS + "/%s" % corpus )
	command = ( "wget http://carrels.distantreader.org/library/%s/study-carrel.zip -O " + CARRELS + "/%s.zip" )
	os.system( command % ( corpus, corpus ) )
	command = ( "unzip " + CARRELS + "/%s.zip -d " + CARRELS + "/%s > /dev/null" )
	os.system( command % ( corpus, corpus ) )

# slurp up the study carrel
for path in glob.glob( CARRELS + '/%s/*/pos/*.pos' % corpus ) :
	try    : df = pd.read_csv( path, sep='\t' )
	except : continue
	else   : break

noun       = df[ df[ 'pos' ] == POS ]
number     = noun.lemma.value_counts()
clean_noun = list( set( [ remove_puncutation( word ) for word in noun.lemma ] ) )

try    : clean_noun.remove('')
except : pass
noun = noun[ noun[ 'lemma' ].isin( clean_noun ) ]

result = pd.DataFrame( list( combinations( clean_noun, 2 ) ), columns=[ 'token1', 'token2' ] )
result[ 'weight' ] = np.zeros( result.shape[ 0 ] )
result = result.loc[ result.index[ : result.shape[ 0 ] ] ]

# count
for i in noun.sid.unique() :
	temp       = noun[ noun[ 'sid' ] == i ]
	temp_lemma = list(set(combinations(temp.lemma.values, 2)))
	for i in temp_lemma :
		value_to_be_add = result[ ( result[ 'token1' ] == i[ 0 ] ) & ( result[ 'token2' ] == i[ 1 ] ) ]
		result.loc[ value_to_be_add.index, 'weight' ] += 1
		value_to_be_add = result[ ( result[ 'token1' ] == i[ 1 ] ) & ( result[ 'token2' ]==i[ 0 ] ) ]
		result.loc[ value_to_be_add.index, 'weight' ] += 1

clean_result  = result[ result[ 'weight' ] > WEIGHT ]
data          = {}
data['nodes'] = []
data['links'] = []

for token in clean_noun :
	size = int( number.loc[ token ] )
	if size > 0 : data[ 'nodes' ].append( { "id":token, "group":1, "size": size } )
for row in clean_result.iterrows() : data[ 'links' ].append( { "source" : row[ 1 ].token1, "target":row[ 1 ].token2, "value":row[ 1 ].weight } )

# output and done
print( json.dumps( data, indent=2 ) )
exit()
