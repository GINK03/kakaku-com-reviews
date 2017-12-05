import os

import json

import pickle

import gzip

import glob

import re

import bs4

import concurrent.futures


def _map(arr):
  key, names = arr

  type_boxs = []
  for name in names:
    soup = bs4.BeautifulSoup( open(name).read() )
    #print( soup.text.replace('\n', '') ) 
    boxs = []
    for box in soup.find_all('div', {'class':'boxIn clearfix minH'}):
      boxs.append( re.sub(r'\s{1,}', ' ', box.text ) )
    if boxs == []:
      continue
    srcs = [ x['src'] for x in filter(lambda x:x is not None and 'bbs' in x['src'], [ title.find('img') for title in soup.find_all('div', {'class':'title'}) ] ) ]
    #print( boxs )
    #print(srcs)

    if len(boxs) != len(srcs):
      continue

    for src, box in zip(srcs,boxs):
      types = src[-5:]
      print(key, types, src,box)
      type_boxs.append( {'types':types, 'box':box} )
  open('parsed/{}.json'.format(key), 'w').write( json.dumps(type_boxs, indent=2, ensure_ascii=False) )

arrs = {}
for index, name in enumerate(glob.glob('../minio-s3/kakaku-com-htmls-20171205-snapshot/*')):
  if 'bbs.kakaku.com' not in name:
    continue
  print(name)
  key = index%100
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append(name)
arrs = [(key,names) for key, names in arrs.items() ]

with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
  exe.map(_map, arrs)

