import sys
import numpy as np
from tree import Tree

G={}
X={}

testSents=[]

def addTree(chart,tag,cell,tree):
    if '^X' in tag:
        tree.c=tag
        tree.ch=[]
        terminal=Tree()
        terminal.c=cell[(tag,)][1]
        terminal.ch=[]
        tree.ch.append(terminal)
    else:
        tree.c=tag
        tree.ch=[]

        bestRule=(tag,'','')
        bestProb=-100000000000000000000000

        for tagEq in cell.keys():
            if tagEq[0]==tag and cell[tagEq][0]>bestProb:
                bestRule=tagEq
                bestProb=cell[tagEq][0]
        
        tagA=cell[bestRule][1][0]
        tagB=cell[bestRule][1][1]

        cellA=chart[cell[bestRule][2][0][0],cell[bestRule][2][0][1]]
        cellB=chart[cell[bestRule][2][1][0],cell[bestRule][2][1][1]]

        r=Tree()
        tree.ch.append(r)
        s=Tree()
        tree.ch.append(s)

        addTree(chart,tagA,cellA,r)
        addTree(chart,tagB,cellB,s)
        

with open(sys.argv[1], 'r') as file:
    for line in file:
        line=line.strip()
        line=line[0:line.index(' : ')]+line[line.index(' : ')+2:len(line)]
        info=line.split(' ')
        if info[0]=='G':
            if (info[2],info[3]) not in G.keys():
                G[(info[2],info[3])]={}
            G[(info[2],info[3])][info[1]]=float(info[4])
        elif info[0]=='X':
            if info[2] not in X.keys():
                X[info[2]]={}
            X[info[2]][info[1]]=float(info[3])

with open(sys.argv[2], 'r') as test:
    for line in test:
        testSents.append(line.strip().split(' '))

with open('output.parses','w') as outPut:
    for i in range(0,len(testSents)):
        sequence=testSents[i]
        dim=len(sequence)+1
        #unkify
        for j in range(0,len(sequence)):
            if sequence[j] not in X.keys():
                sequence[j]='<unk>'
        chart=np.zeros((dim,dim),dtype='object')
        #Initialization
        for col in range(1,dim):
            word=sequence[col-1]
            probs={}
            for tag in X[word].keys():
                probs[(tag,)]=(X[word][tag],word)
            chart[col-1,col]=probs
        #Induction
        for col in range(2,dim):
            for row in range(dim-(dim-col+2),-1,-1):
                possibleSub={}
                for j in range(col-1,row,-1):
                    A=chart[row,j]
                    B=chart[j,col]
                    for const0 in A.keys():
                        for const1 in B.keys():
                            tag0=const0[0]
                            tag1=const1[0]
                            Aprob=A[const0][0]
                            Bprob=B[const1][0]
                            if (tag0,tag1) in G.keys():
                                for tag in G[(tag0,tag1)].keys():
                                    if (tag,tag0,tag1) not in possibleSub.keys() or possibleSub[(tag,tag0,tag1)][0]<G[(tag0,tag1)][tag]+Aprob+Bprob:
                                        possibleSub[(tag,tag0,tag1)]=(G[(tag0,tag1)][tag]+Aprob+Bprob,(tag0,tag1),((row,j),(j,col)))
                chart[row,col]=possibleSub
        #argmax
        bestTag=('','','')
        bestProb=-100000000000000000000000
        for tag in chart[0,dim-1].keys():
            if  'ROOT' in tag[0] and '|' not in tag[0] and chart[0,dim-1][tag][0]>bestProb:
                bestTag=tag
                bestProb=chart[0,dim-1][tag][0]
        if not(bestTag==('','','')):
            outPut.write('LL'+str(i)+': '+str(bestProb)+'\n')
            parse=Tree()
            addTree(chart,bestTag[0],chart[0,dim-1],parse)
            outPut.write(str(parse)+'\n')
        else:
            outPut.write('LL'+str(i)+': nan\n')
            outPut.write('FAIL\n')