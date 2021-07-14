import io
import re
from collections import defaultdict

poscomment = []
negcomment = []
dicpos = defaultdict(list)
dicneg = defaultdict(list)
dicposbin = defaultdict(list)
dicnegbin= defaultdict(list)


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
        if ii not in dicpos.keys():
            dicpos[ii].append(0)

        if len(ii) >= 2:
            dicpos[ii][0] += 1

for i in poscomment:
    for ii in range(len(i)):
        if ii == (len(i) - 1):
            break
        if len(i[ii]) < 3 or  len(i[ii+1]) < 3:
            continue
        binary = i[ii] +" "+ i[ii+1]
        if binary not in dicposbin.keys():
            dicposbin[binary].append(0)

        if len(binary) > 5:
            dicposbin[binary][0] += 1



for i in poscomment:
    for ii in i:
        if ii in dicpos.keys():
            if dicpos[ii][0] > 10 or dicpos[ii][0]  < 3:
                dicpos.pop(ii)

for i in poscomment:
    for ii in range(len(i)):
        if ii == (len(i) - 1):
            break
        binary = i[ii] +" "+ i[ii+1]
        if binary in dicposbin.keys():
            if dicposbin[binary][0] > 10 or dicposbin[binary][0]  < 3:
                dicposbin.pop(binary)



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
        if ii not in dicneg.keys():
            dicneg[ii].append(0)

        if len(ii) >= 2:
            dicneg[ii][0] += 1


for i in negcomment:
    for ii in range(len(i)):
        if ii == (len(i) - 1):
            break
        if len(i[ii]) < 3 or  len(i[ii+1]) < 3:
            continue
        binary = i[ii] +" "+ i[ii+1]
        if binary not in dicnegbin.keys():
            dicnegbin[binary].append(0)

        if len(binary) > 5:
            dicnegbin[binary][0] += 1


for i in negcomment:
    for ii in i:
        if ii in dicneg.keys():
            if dicneg[ii][0] >= 10 or dicneg[ii][0]  <= 2:
                dicneg.pop(ii)


for i in negcomment:
    for ii in range(len(i)):
        if ii == (len(i) - 1):
            break
        binary = i[ii] +" "+ i[ii+1]
        if binary in dicnegbin.keys():
            if dicnegbin[binary][0] > 10 or dicnegbin[binary][0]  < 3:
                dicnegbin.pop(binary)

