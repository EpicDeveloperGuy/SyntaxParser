import sys
import re
import numpy as np
from tree import Tree

known=set()

G={}
X={}

Gg={}
Xx={}

forrest=[]
def addDic(key,dic):
    if not(key in dic.keys()):
        dic[key]=1
    else:
        dic[key]+=1

def addSet(val,setto):
    if not(val in setto):
        setto.add(val)

def collapse(syntaxTree):
    if syntaxTree.ch==[]:
        return '^X'
    if len(syntaxTree.ch)==1:
        yeet=collapse(syntaxTree.ch[0])
        if len(syntaxTree.ch[0].ch)>=1:
            syntaxTree.ch=syntaxTree.ch[0].ch
            syntaxTree.c+='+'
        syntaxTree.c+=yeet
        return syntaxTree.c
    else:
        for child in syntaxTree.ch:
            collapse(child)
        return syntaxTree.c

def traverse(syntaxTree):
    #preterminal
    if len(syntaxTree.ch)==1:
        if not(syntaxTree.c in X.keys()):
            X[syntaxTree.c]={}
        addDic(syntaxTree.ch[0].c,X[syntaxTree.c])
        addDic(syntaxTree.c,Xx)
        addSet(syntaxTree.ch[0].c,known)
        addSet(syntaxTree.c,known)
    #fix this part
    else:
        if not(syntaxTree.c in G.keys()):
            G[syntaxTree.c]={}
        children=(syntaxTree.ch[0].c,syntaxTree.ch[1].c)
        addDic(children,G[syntaxTree.c])
        addDic(syntaxTree.c,Gg)
        addSet(syntaxTree.c,known)
        for child in syntaxTree.ch:
            traverse(child)
            

def unkTraverse(syntaxTree):
    #word
    if syntaxTree.ch==[]:
        if not(syntaxTree.c in known):
            syntaxTree.c='<unk>'
    #rest
    else:
        if not(syntaxTree.c in known):
            if len(syntaxTree.ch)==1:
                syntaxTree.c='<unk>^X'
            else:
                syntaxTree.c='<unk>'
        for child in syntaxTree.ch:
            unkTraverse(child)

with open(sys.argv[1], 'r') as superFile:
    treeText=''
    for line in superFile.readlines():
        treeText+=line.strip()+' '
    while len(treeText)>0:
        try:
            j=re.search('\(ROOT[^|]',treeText[1:len(treeText)]).start()+1
        except:
            j=len(treeText)
        treeFy=treeText[0:j]
        treeText=treeText[j:len(treeText)]
        syntaxTree=Tree()
        syntaxTree.read(treeFy)
        forrest.append(syntaxTree)

percent=float(sys.argv[2])

i=0
while i<np.floor(percent*len(forrest)):
    collapse(forrest[i])
    traverse(forrest[i])
    i+=1
while i<len(forrest):
    collapse(forrest[i])
    unkTraverse(forrest[i])
    traverse(forrest[i])
    i+=1

with open('model.pcfg', 'w') as outPut:
    for parent in G.keys():
        for children in G[parent].keys():
            outPut.write('G '+parent+' : '+children[0]+' '+children[1]+' '+str(np.log(G[parent][children]/Gg[parent]))+'\n')
    for tag in X.keys():
        for obs in X[tag].keys():
            outPut.write('X '+tag+' : '+obs+' '+str(np.log(X[tag][obs]/Xx[tag]))+'\n')