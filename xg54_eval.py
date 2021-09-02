import sys
from tree import Tree

ourParses=[]
goldParses=[]

def treeSpans(spans,tree):
    if len(tree.ch)==1:
        spans.append(treeSpan(tree))
    else:
        spans.append(treeSpan(tree))
        treeSpans(spans,tree.ch[0])
        treeSpans(spans,tree.ch[1])

def treeSpan(tree):
    if len(tree.ch)==1:
        return (tree.ch[0].c,)
    else:
        return treeSpan(tree.ch[0])+treeSpan(tree.ch[1])

def standardTerms(terms,tree):
    if len(tree.ch)==1:
        tree.ch[0].c='word'+str(len(terms))
        terms.append('')
    else:
        standardTerms(terms,tree.ch[0])
        standardTerms(terms,tree.ch[1])

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

with open(sys.argv[1],'r') as ourParse:
    lines=ourParse.readlines()
    for i in range(0,len(lines)):
        if i%2==1:
            ourParses.append(lines[i].strip())
with open(sys.argv[2],'r') as goldParse:
    for line in goldParse.readlines():
        goldParses.append(line.strip())

with open('output.eval','w') as outPut:
    for i in range(0,len(ourParses)):
        P=0.0
        R=0.0
        F=0.0
        if not(ourParses[i]=='FAIL'):
            ourTree=Tree()
            ourTree.read(ourParses[i])
            goldTree=Tree()
            goldTree.read(goldParses[i])

            #collapse gold parse
            collapse(goldTree)

            #standardize the words to nums
            ourTerms=[]
            standardTerms(ourTerms,ourTree)
            goldTerms=[]
            standardTerms(goldTerms,goldTree)

            ourSpans=[]
            treeSpans(ourSpans,ourTree)
            goldSpans=[]
            treeSpans(goldSpans,goldTree)

            numCorrect=0

            for const in ourSpans:
                if const in goldSpans:
                    numCorrect+=1
            
            P=numCorrect/len(ourSpans)
            R=numCorrect/len(goldSpans)
            F=2*P*R/(P+R)

        outPut.write('P '+str(P)+';R '+str(R)+';F '+str(F)+'\n')
        