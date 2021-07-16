import io
import re
import copy
from collections import defaultdict

poscomment = []
negcomment = []
dicpos = defaultdict(list)
dicneg = defaultdict(list)
dicposbin = defaultdict(list)
dicnegbin= defaultdict(list)
spanlist = []



def extract_data(kind):

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

    return commentlist


def build_unigram(kind):
    commentlist = None
    unidic = None
    if kind == "pos":
        commentlist = poscomment
        unidic = dicpos
    else:
        commentlist = negcomment
        unidic = dicneg
        
    for i in commentlist:
        for ii in i:
            # if len(ii) >= 2:
            if ii not in unidic.keys():
                unidic[ii].append(0)
            unidic[ii][0] += 1



def remove_lowpowers(kind):
    commentlist = None
    unidic = None
    if kind == "pos":
        commentlist = poscomment
        unidic = dicpos
    else:
        commentlist = negcomment
        unidic = dicneg
   
    for i in commentlist:
        for ii in i:
            if ii in unidic.keys():
                if unidic[ii][0] > 10 or unidic[ii][0]  < 2:
                    spanlist.append(ii)
                    unidic.pop(ii)

def process_file(kind):
    commentlist = None
    if kind == "pos":
        commentlist = poscomment
    else:
        commentlist = negcomment
    newOne = []
    for i in commentlist:
        row = []
        for ii in i:
            # if len(ii) >= 2:
            if ii not in spanlist:
                row.append(ii)
        newOne.append(row)
    return newOne


def build_bigram(kind):
    commentlist = None
    bindic = None
    if kind == "pos":
        commentlist = poscomment
        bindic = dicposbin
    else:
        commentlist = negcomment
        bindic = dicnegbin

    for i in commentlist:
        for ii in range(len(i)):
            if ii == (len(i) - 1):
                break
           
            binary = i[ii] +" "+ i[ii+1]
            if binary not in bindic.keys():
                bindic[binary].append(0)
    
            
            bindic[binary][0] += 1
    

    

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
    print("hi")
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
        # print(n)
        # print(wi_1)
        # print(dicUnigram[wi_1])
        p = dicBigram[n][0] / dicUnigram[wi_1][0] 
        format_float = "{:.6f}".format(p)
        dicBigram[n].append(format_float)




poscomment = extract_data("pos")
build_unigram("pos")
remove_lowpowers("pos")
poscomment = process_file("pos")
build_bigram("pos")
cal_P_Unigram("pos")
cal_P_bigram("pos")

negcomment = extract_data("neg")
build_unigram("neg")
remove_lowpowers("neg")
negcomment = process_file("neg")
build_bigram("neg")
cal_P_Unigram("neg")
cal_P_bigram("neg")

print(dicnegbin)

