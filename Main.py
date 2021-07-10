import io
import re
from collections import defaultdict

poscomment = []
negcomment = []
dicpos = defaultdict(int)
dicneg = defaultdict(int)

address = ".\Sources\\rt-polarity.pos"
with open(address) as reader :
    myinput = reader.read()

buf = io.StringIO(myinput)
line = buf.readline()

while line != "":
    line = re.sub(",|\?|\.|\[|\]|\"|-|;|:|\(|\)|\\|_|\*|&|\^|\$|!|'|\/|–" , " " , line)
    line = re.sub("\s{2,}"," ",line)
    line = re.sub("\n","",line)
    # buffread = re.findall("[a-zA-Z0-9]+", line)
    buffread = re.findall("[a-zA-Z]+", line)
    poscomment.append(buffread)
    line = buf.readline()


for i in poscomment:
    for ii in i:
        if len(ii) >= 2:
            dicpos[ii] += 1

for i in poscomment:
    for ii in i:
        if dicpos[ii] >= 10 or dicpos[ii]  <= 2:
            dicpos.pop(ii)



address = ".\Sources\\rt-polarity.neg"
with open(address) as reader :
    myinput = reader.read()

buf = io.StringIO(myinput)
line = buf.readline()

while line != "":
    line = re.sub(",|\?|\.|\[|\]|\"|-|;|:|\(|\)|\\|_|\*|&|\^|\$|!|'|\/|–" , " " , line)
    line = re.sub("\s{2,}"," ",line)
    line = re.sub("\n","",line)
    buffread = re.findall("[a-zA-Z]+", line)
    negcomment.append(buffread)
    line = buf.readline()


for i in negcomment:
    for ii in i:
        if len(ii) >= 2:
            dicneg[ii] += 1

for i in negcomment:
    for ii in i:
        if dicneg[ii] >= 10 or dicneg[ii]  <= 2:
            dicneg.pop(ii)



