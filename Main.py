import io
import re
from collections import defaultdict

poscomment = []
negcomment = []
dicpos = defaultdict(list)
dicneg = defaultdict(list)
dicposbin = defaultdict(list)
dicnegbin= defaultdict(list)
# M_neg = 0
# M_pos = 0



def extract_data(kind , unidic , bindic):

    commentlist = list()

    if kind == "pos":
        address = ".\Sources\\rt-polarity.pos"
    else:
        address = ".\Sources\\rt-polarity.neg"

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
        commentlist.append(buffread)
        line = buf.readline()

    for i in commentlist:
        for ii in i:
            if ii not in unidic.keys():
                unidic[ii].append(0)

            if len(ii) >= 2:
                unidic[ii][0] += 1

    for i in commentlist:
        for ii in range(len(i)):
            if ii == (len(i) - 1):
                break
            if len(i[ii]) < 3 or  len(i[ii+1]) < 3:
                continue
            binary = i[ii] +" "+ i[ii+1]
            if binary not in bindic.keys():
                bindic[binary].append(0)
    
            if len(binary) > 5:
                bindic[binary][0] += 1
    
    
    for i in commentlist:
        for ii in i:
            if ii in unidic.keys():
                if unidic[ii][0] > 10 or unidic[ii][0]  < 3:
                    unidic.pop(ii)
    
    for i in commentlist:
        for ii in range(len(i)):
            if ii == (len(i) - 1):
                break
            binary = i[ii] +" "+ i[ii+1]
            if binary in bindic.keys():
                if bindic[binary][0] > 10 or bindic[binary][0]  < 3:
                    bindic.pop(binary)
                    continue
                if i[ii+1] not in unidic.keys() :
                    unidic[i[ii+1]].append(1)
                if i[ii+1] not in unidic.keys() :
                    unidic[i[ii+1]].append(1)

    

def cal_M(kind):
    dicM = None
    sumM = 0
    if kind == "pos" :
        dicM = dicpos
    else:
        dicM = dicneg
    for n in dicM.values():
        sumM += n[0]
    
    return sumM

        

def cal_P_Unigram(kind):
    dicP = None
    M = 0
    if kind == "pos":
        dicP = dicpos
        M = cal_M("pos")
    else:
        dicP = dicneg
        M = cal_M("neg")

    for n in dicP.values():
        p =n[0] / M
        format_float = "{:.6f}".format(p)
        n.append(format_float)

def cal_P_bigram(kind):
    dicUnigram = None
    dicBigram = None
    if kind == "pos":
        dicUnigram = dicpos
        dicBigram = dicposbin
    else:
        dicUnigram = dicneg
        dicBigram = dicnegbin

    for n in dicBigram.keys():
        wi_1 = n.split(" ")[1]
        print(n)
        print(wi_1)
        print(dicUnigram[wi_1])
        # p = dicBigram[n][0] / dicUnigram[wi_1][0] 
        # format_float = "{:.6f}".format(p)
        # dicBigram[n].append(p)


extract_data("pos" , dicpos , dicposbin)
extract_data("neg" , dicneg , dicnegbin)
# print(dicnegbin)
# print(dicneg)
# print(cal_M("neg"))
# cal_P_bigram("pos")
# print(dicpos)
print("strength" in dicpos)
print("the strength" in dicposbin)
# print(dicneg["strength"])
print(dicposbin["the strength"])
print(dicpos["strength"])