import json


f = open('./data.txt.model')

[next(f) for i in range(6)]

term_index = json.loads( open('term_index.json').read() )
index_term = {index:term for term, index in term_index.items() }

feat_weight = {}
for index, line in enumerate(f):
  line = line.strip()
  feat_weight[index_term[index+1]] = float(line)

for feat, weight in sorted(feat_weight.items(), key=lambda x:x[1]*-1):
  print(feat, weight)
