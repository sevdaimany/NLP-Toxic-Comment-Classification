import io
import re
import copy
from collections import defaultdict

poscomment = []
negcomment = []
testpos = []
testneg = []
dicpos = defaultdict(list)
dicneg = defaultdict(list)
dicposbin = defaultdict(list)
dicnegbin= defaultdict(list)
spanlist = []

l1 , l2 , l3 = 0.6 , 0.3 , 0.1
E = 0.00001

def extract_data(kind):

    commentlist = list()
    count = 0

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
        buffread = re.findall("[a-zA-Z]{3,}", line)

        if count > 5200 :
            if kind == "pos":
                testpos.append(buffread)
            else:
                testneg.append(buffread)
        else:
            commentlist.append(buffread)

        line = buf.readline()
        count += 1
 
    return commentlist

def extract_data_comment(line):
    
    line = re.sub(",|\?|\.|\[|\]|\"|-|;|:|\(|\)|\\|_|\*|&|\^|\$|!|'|\/|–" , " " , line)
    line = re.sub("\s{2,}"," ",line)
    line = re.sub("\n","",line)

    return re.findall("[a-zA-Z]{3,}", line)


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
                if unidic[ii][0] > 20 or unidic[ii][0]  < 2:
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


def find_unigram(cmnt , kind):

    p = 1
    p1 ,p2 = 0 ,0 

    if kind == "pos" and cmnt in dicpos.keys():
        p2 = float(dicpos[cmnt][1])

    elif kind == "neg" and cmnt in dicneg.keys():
        p2 = float(dicneg[cmnt][1])

    p = l2*p2 + l3*E
    return p
    
def find_bigram(cmnt , kind):
    p = 1
    p1 ,p2 = 0 ,0 

    if kind == "pos":
        if cmnt in dicposbin.keys():
            p1  = float(dicposbin[cmnt])
        if cmnt in dicpos.keys():
            p2 = float(dicpos[cmnt])

    elif kind == "neg":
        if cmnt in dicnegbin.keys():
            p1  = float(dicnegbin[cmnt])
        if cmnt in dicneg.keys():
            p2 = float(dicneg[cmnt])

    p = l1*p1 + l2*p2 + l3*E
    return p

def calculate_p(comment , model):

    ppos = 0.5
    pneg = 0.5

    for cmnt in comment:
        if model == "bigram":
            iindex = comment.index(cmnt)
            if iindex == 0:

                ppos *= find_unigram(cmnt , "pos")
                pneg *= find_unigram(cmnt , "neg")
                continue
            
            wib = comment[iindex - 1]
            w = wib + " " + cmnt

            ppos *= find_bigram(w , "pos")
            pneg *= find_bigram(w , "neg")

        else:
            ppos *= find_unigram(cmnt , "pos")
            pneg *= find_unigram(cmnt , "neg")
    
    return ppos ,pneg
    

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

model = "unigram"
# model = "bigram"

# comment = extract_data_comment(input())
# ppos ,pneg = calculate_p(comment , model)

for comment in testpos:
    ppos ,pneg = calculate_p(comment , model)
    if ppos >= pneg :
        print("not filter this")
    else : 
        print("filter this")


# if ppos >= pneg :
#     print("not filter this")
# else : 
#     print("filter this")


