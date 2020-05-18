import sys
import numpy as np
from collections import OrderedDict

gop_score = sys.argv[1]
hum_score = sys.argv[2]

gop1 = {}
gop2 = {}
gop3 = {}
with open(gop_score, 'r') as f:
    for line in f:
        l = line.strip().split()
        gop1[l[0]] = float(l[1])
        gop2[l[0]] = float(l[2])
        gop3[l[0]] = float(l[3])

hum = {}
with open(hum_score, 'r') as f:
    for line in f:
        l = line.strip().split()
        hum[l[0]] = float(l[1])

gop1_v = []
gop2_v = []
gop3_v = []
hum_v = []
for k in sorted(gop1.keys()):
    gop1_v.append(gop1[k])
    gop2_v.append(gop2[k])
    gop3_v.append(gop3[k])
    hum_v.append(hum[k])

print('Pearson correlation between human scores and three types of GOP scores seperately:')
print(np.corrcoef(np.array(hum_v), np.array(gop1_v))[0][1])
print(np.corrcoef(np.array(hum_v), np.array(gop2_v))[0][1])
print(np.corrcoef(np.array(hum_v), np.array(gop3_v))[0][1])