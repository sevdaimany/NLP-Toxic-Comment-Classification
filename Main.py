import io


address = ".\puzzles\puzzle3.txt"
with open(address) as reader :
    myinput = reader.read()


buf = io.StringIO(myinput)
n , m = map(int ,buf.readlines(1)[0].replace("\t" , " ").replace("\n" , "").split(" "))
for i in range(n):
    buffread = buf.readlines(1)[0].replace("\t" , " ").replace("\n" , "").split(" ")
    mynd = []
    for ii in range(m) : 
        mynd.append(buffread[ii])
    mypuzzle.append(mynd)