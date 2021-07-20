import io
import re
import copy
from collections import defaultdict

poscomment = []
negcomment = []
testpos = []
testneg = []
spamwords = []
dicpos = defaultdict(list)
dicneg = defaultdict(list)
dicposbin = defaultdict(list)
dicnegbin= defaultdict(list)
spanlist = []
defualtComments = True
numberOfComments = 0
numNeg =0
numPos = 0

l1 , l2 , l3 = 0.8 , 0.15 , 0.05
E = 0.0001

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
        buffread = re.findall("[a-zA-Z]{1,}", line)


        if defualtComments == True :
            if count > numberOfComments :
                if kind == "pos":
                    testpos.append(buffread)
                else:
                    testneg.append(buffread)
            else:
                commentlist.append(buffread)
        else:
            commentlist.append(buffread)


        line = buf.readline()
        count += 1
 
    return commentlist

def extract_data_comment(line):
    
    line = re.sub(",|\?|\.|\[|\]|\"|-|;|:|\(|\)|\\|_|\*|&|\^|\$|!|'|\/|–" , " " , line)
    line = re.sub("\s{2,}"," ",line)
    line = re.sub("\n","",line)

    return re.findall("[a-zA-Z]{1,}", line)


def extract_spam():

    address = ".\Sources\\spamwords.txt"
    with open(address) as reader :
        myinput = reader.read()

    buf = io.StringIO(myinput)
    line = buf.readline()

    while line != "":
        line = line.replace("\n","")
        line = line.replace("  "," ")
        buffread = line.split(" ")
        spamwords.extend(buffread)
        line = buf.readline()

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
                if ii in spamwords or unidic[ii][0]  < 2:
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
        n.append(p)

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
        wi_1 = n.split(" ")[0]
        p = dicBigram[n][0] / dicUnigram[wi_1][0] 
        dicBigram[n].append(p)


def find_unigram(cmnt , kind):

    p = 1
    p2 = 0

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
            p1  = dicposbin[cmnt][1]
        if cmnt in dicpos.keys():
            p2 = dicpos[cmnt][1]

    elif kind == "neg":
        if cmnt in dicnegbin.keys():
            p1  = dicnegbin[cmnt][1]
        if cmnt in dicneg.keys():
            p2 = dicneg[cmnt][1]

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



def process_comment(comment):
    for c in comment:
        if c in spamwords:
            comment.remove(c)

    return comment


model = ""
typee = ""

print("1)unigram\n2)bigram")
inbu = int(input())
if inbu ==2 :
    model = "bigram"
else:
    model = "unigram"

print("1)Give comments yourself\n2)Use our default comments for checking")
in2 = int(input())
if in2 ==1 :
    typee = "tests"
    defualtComments = False
else:
    print("number of comments : ")
    n = int(input())
    # print("n ", n)
    numberOfComments = 5331 - n -1
    typee = "test"
    defualtComments = True


print("wait")
extract_spam()
poscomment = extract_data("pos")
build_unigram("pos")
# remove_lowpowers("pos")
# poscomment = process_file("pos")
build_bigram("pos")
cal_P_Unigram("pos")
cal_P_bigram("pos")

negcomment = extract_data("neg")
build_unigram("neg")
# remove_lowpowers("neg")
# negcomment = process_file("neg")
build_bigram("neg")
cal_P_Unigram("neg")
cal_P_bigram("neg")
print("done!")




if typee == "test":
    coun = 0
    sums = 0

    c = 0
    print()
    for comment in testneg:
        c += 1
        print(c,") " ,' '.join(map(str, comment)))
        sums +=1
        ppos ,pneg = calculate_p(comment , model)
        if ppos >= pneg :
            print("not filter this")
        else : 
            print("filter this")
            coun+=1
        print()

    print("Percentage : ",(coun / sums) * 100 , " %")
else:
    
    myinput = input()
    while not myinput == "exit":
        comment = extract_data_comment(myinput)
        comment = process_comment(comment)
        ppos ,pneg = calculate_p(comment , model)

        if ppos >= pneg :
            print("not filter this")
        else : 
            print("filter this")
        
        myinput = input()





    
    


