import re
import sys

# a Tree consists of a category label 'c' and a list of child Trees 'ch'
class Tree:
    
    # obtain tree from string
    def read(self,s):
        self.ch = []
        # a tree can be just a terminal symbol (a leaf)
        m = re.search('^ *([^ ()]+) *(.*)',s)
        if m != None:
            self.c = m.group(1)
            return m.group(2)
        # a tree can be an open paren, nonterminal symbol, subtrees, close paren
        m = re.search('^ *\( *([^ ()]*) *(.*)',s)
        if m != None:
            self.c = m.group(1)
            s = m.group(2)
            while re.search('^ *\)',s) == None:
                t = Tree()
                s = t.read(s)
                self.ch = self.ch + [t]
            return re.search('^ *\) *(.*)',s).group(1)
        return ''

    # obtain string from tree
    def __str__(self):
        if self.ch == []:
            return self.c
        s = '(' + self.c
        for t in self.ch:
            s = s + ' ' + str(t)
        return s + ')'
