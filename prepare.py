import sys

import json

import pickle

import gzip

import glob

from collections import Counter

import math

import MeCab 

import re
if '--wakati1' in sys.argv:
  m = MeCab.Tagger('-Owakati')

  data = []
  for name in glob.glob('parsed/*.json'):
    print(name)
    objs = json.loads( open(name).read() )
    for obj in objs:
      types = obj['types'] 
      box = m.parse(obj['box']).strip().split()
      box = [ b for b in box if re.search(r'^\d{1,}$', b) is None ]
      term_freq = dict(Counter(box))
      data.append( (types, term_freq) )

  open('wakati1.json', 'w').write( json.dumps(data, indent=2, ensure_ascii=False) )

if '--trigram1' in sys.argv:
  data = []
  for name in sorted( glob.glob('parsed/*.json') )[:20]:
    print(name)
    objs = json.loads( open(name).read() )
    for obj in objs:
      types = obj['types'] 
      text = obj['box']
      size = len(text)
      box = []
      for i in range(size-1):
        box.append( text[i:i+1] )
      term_freq = dict(Counter(box))
      data.append( (types, term_freq) )
  open('wakati1.json', 'w').write( json.dumps(data, indent=2, ensure_ascii=False) )
  
if '--term_index1' in sys.argv:
  wakatis = json.loads( open('wakati1.json').read() ) 
  terms = set()
  for types, term_freq in wakatis:
    [ terms.add(term) for term in list(term_freq.keys()) ]

  term_index = {}

  for index, term in enumerate(terms):
    term_index[term] = index
  
  open('term_index.json', 'w').write( json.dumps(term_index,indent=2,ensure_ascii=False) )

if '--vectorize1' in sys.argv:
  wakatis = json.loads( open('wakati1.json').read() ) 
  term_index = json.loads( open('term_index.json').read() )

  f = open('data.txt', 'w')
  for types, term_freq in wakatis:
    if types in ['1.gif', '2.gif', '5.gif'] :
      flags = 1.0
    else:
      flags = 0.0
    vec = ' '.join( ['{}:{}'.format(term_index[term], math.log(freq+1.0)) for term, freq in sorted(term_freq.items(), key=lambda x:term_index[x[0]]) if term_index[term] != 0 ] )
    data = '{} {}'.format(flags, vec)
    f.write( data + '\n' )
