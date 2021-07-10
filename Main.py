import io
import re

poscomment = []
negcomment = []


address = ".\Sources\\rt-polarity.pos"
with open(address) as reader :
    myinput = reader.read()



buf = io.StringIO(myinput)
line = buf.readline()

while line != "":
    line = re.sub(",|\?|\.|\[|\]|\"|-|;|:|\(|\)|\\|_|\*|&|\^|\$|!" , " " , line)
    line = re.sub("\s{2,}"," ",line)
    line = buf.readline()

    

# for i in poscomment:
#     print(poscomment)

