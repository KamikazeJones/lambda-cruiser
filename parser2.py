#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node:

    def __init__(self,typ,left,right):
        self.typ   = typ
        self.left  = left
        self.right = right

    def traverse(self):
        if self.typ=='L':
            return "< "+self.left.traverse() +" "+self.right.traverse()+" >"
        elif self.typ=='A':
            return "( "+self.left.traverse()+" "+self.right.traverse()+" )"
        elif self.typ == 'V':
            return self.left # es ist Variable

    def copy(self):
        if self.typ=='L' or self.typ == 'A':
            return Node(self.typ[:], self.left.copy(), self.right.copy())
        elif self.typ == 'V':
            return Node('V', self.left[:],None) # es ist Variable

    def FV(self):
        if self.typ == 'A':
            return self.left.FV()+self.right.FV()
        elif self.typ == 'L':
            rfv = self.right.FV()
            v = self.left.left
            return [x for x in rfv if x != v]
        elif self.typ == 'V':
            return [self.left]
        

    def substitute(self, repl, x, parent): # Ersetzung erfolgt "in place"
        if self.typ == 'A': # Applikation
            self.left.substitute(repl, x, self)
            self.right.substitute(repl, x, self)
        elif self.typ == 'L': # lambda-Abstraktion <y r>
            y,r = self.left.left, self.right
            if x != y:
                i=0; y1=y
                fv = repl.FV()
                while y1 in fv: # print "Namenskonflikt! %s in %s" % (y1, repl.traverse())
                    i+=1; y1=y+str(i)
                if i>0:
                    self.left.left = y1
                    r.substitute(Node('V',y1,None), y, self)
                r.substitute(repl, x, self)
          # else: hier wird nix ersetzt, da x durch x ersetzt werden soll
                
        elif self.typ == 'V': # einfache Variable
            if x==self.left:
                if parent.left == self:
                    parent.left = repl.copy()
                else:
                    parent.right = repl.copy()                     

    # def betaReductionByValue(self, parent):
        # if self.typ == 'A':
            # t1,t2 = self.left, self.right
            # t1.betaReductionByValue(self)
            # t1 = self.left
            # t2.betaReductionByValue(self)
            # t2 = self.right
            # if t1.typ == 'L':
                # y,r = t1.left.left, t1.right
                # print "substitute (bv) "+r.traverse()+": ersetze "+y+" mit "+t2.traverse()
                # r.substitute(t2, y, t1)
                # t1.right.betaReductionByValue(t1)
                # if parent.left == self:
                    # parent.left = t1.right
                # else:
                    # parent.right = t1.right
        # else:
            # return False # keine Ersetzung (Variable + Lambda)

    def betaReductionByValueToWeakNF(self, parent):
        # print "bv: "+self.traverse()
        if self.typ == 'V':
            # print "V -- betaReductionByValueToWeakNF"
            # x --bv--> x
            return # Variable x durch x ersetzen: keine Aktion notwendig
        elif self.typ == 'L':
            # print "L -- betaReductionByValueToWeakNF"
            # (λx.e) --bv--> (λx.e)
            return # in Lambda-Ausdrücken nichts ersetzen
        elif self.typ == 'A':
            # print "A -- betaReductionByValueToWeakNF"
            # e1 --bv--> (λx.e)  e2 --bv--> e2'  e[e2'/x] --bv--> e'
            # ------------------------------------------------------
            # ( e1 e2) --bv--> e'
            e1, e2 = self.left, self.right
            e1.betaReductionByValueToWeakNF(self)
            e2.betaReductionByValueToWeakNF(self)
            e1,e2 = self.left,self.right
            if e1.typ == 'L':
                # print "A-L -- betaReductionByValueToWeakNF"
                x,e = e1.left.left, e1.right
                # print "substitute (bv) "+e.traverse()+": ersetze "+x+" mit "+e2.traverse()
                e.substitute(e2,x,e1) # Ergebnis ist nun in e1.right
                e1.right.betaReductionByValueToWeakNF(e1)
                if self == parent.left:
                    parent.left = e1.right
                elif self == parent.right:
                    parent.right = e1.right
                else:
                    print "something is wrong here!"
                    sys.exit()
            else:   
                # print "A-(A or V) -- betaReductionByValueToWeakNF"
                # we have already replaced e1 by e1' and e2 by e2'!
                return

    
    # def betaReductionHybridApplicative(self, parent):
        # if self.typ == 'A':
            # t1,t2 = self.left, self.right
            # t1.betaReductionByValue(self)
            # t1 = self.left
            # t2.betaReductionHybridApplicative(self)
            # t2 = self.right
            # if t1.typ == 'L':
                # y,r = t1.left.left, t1.right
                # print "substitute (ha) "+r.traverse()+": ersetze "+y+" mit "+t2.traverse()
                # r.substitute(t2, y, t1)
                # t1.right.betaReductionHybridApplicative(t1)
                # sys.stdin.read(1)
                # if parent.left == self:
                    # parent.left = t1.right
                # else:
                    # parent.right = t1.right
            # else:
                # t1.betaReductionHybridApplicative(self)
        # elif self.typ == 'L': 
            # self.right.betaReductionHybridApplicative(self)
        # else:
            # return # keine Ersetzung (Variable)


    def betaReductionHybridApplicativeToNF(self,parent):
        # print "ha: "+self.traverse()
        if self.typ == 'V':
            # print "V -- betaReductionHybridApplicativeToNF"
            # x --ha--> x
            return 
        elif self.typ == 'L':
            # print "L -- betaReductionHybridApplicativeToNF"
            #      e --ha--> e'
            # ----------------------
            # (λx.e) --ha--> (λx.e')
            x,e =  self.left.left, self.right
            e.betaReductionHybridApplicativeToNF(self)
        elif self.typ == 'A':
            # print "A -- betaReductionHybridApplicativeToNF"
            # e1 --bv--> (λx.e)  e2 --ha--> e2'  e[e2'/x] --ha--> e'
            # ------------------------------------------------------
            # (e1 e2) --ha--> e'
            e1, e2 = self.left, self.right
        
            e1.betaReductionByValueToWeakNF(self)
            e2.betaReductionHybridApplicativeToNF(self)
            e1, e2 = self.left, self.right
            if(e1.typ == 'L'):
                # print "A-L -- betaReductionHybridApplicativeToNF"
                x, e = e1.left.left, e1.right
                e.substitute(e2,x,e1) # Ergebnis ist nun in e1.right
                e1.right.betaReductionHybridApplicativeToNF(e1)
                if self == parent.left:
                    parent.left = e1.right
                elif self == parent.right:
                    parent.right = e1.right
            else:
                # print "A-(A or V) -- betaReductionHybridApplicativeToNF"
                e1.betaReductionHybridApplicativeToNF(self)
                

##    def betaReductionByValueEtaToWeakNF(self, parent):
##        print "bve: "+self.traverse()
##        if self.typ == 'V':
##            print "V -- betaReductionByValueEtaToWeakNF"
##            # x --bv--> x
##            return # Variable x durch x ersetzen: keine Aktion notwendig
##        elif self.typ == 'L':
##            print "L -- betaReductionByValueEtaToWeakNF"
##            # (λx.e) --bv--> (λx.e)
##            return # in Lambda-Ausdrücken nichts ersetzen
##        elif self.typ == 'A':
##            print "A -- betaReductionByValueEtaToWeakNF"
##            # e1 --bv--> (λx.e)  e2 --bv--> e2'  e[e2'/x] --bv--> e'
##            # ------------------------------------------------------
##            # ( e1 e2) --bv--> e'
##            e1, e2 = self.left, self.right
##            print e1.traverse()
##            print e2.traverse()
##            # if(e1=='L' and e2 == 'V' and e1.left.left == e2.left):
##                  # ((λx.e) x) -->ha--> e
##                  # if self == parent.left:
##                  #     parent.left = e1.right
##                  # else:
##                  #     parent.right = e1.right
##            #      print "Eta-Case"
##        
##            e1.betaReductionByValueEtaToWeakNF(self)
##            e2.betaReductionByValueEtaToWeakNF(self)
##            e1,e2 = self.left,self.right
##            if e1.typ == 'L':
##                print "A-L -- betaReductionByValueEtaToWeakNF"
##                x,e = e1.left.left, e1.right
##                print "substitute (bv) "+e.traverse()+": ersetze "+x+" mit "+e2.traverse()
##                e.substitute(e2,x,e1) # Ergebnis ist nun in e1.right
##                e1.right.betaReductionByValueEtaToWeakNF(e1)
##                if self == parent.left:
##                    parent.left = e1.right
##                elif self == parent.right:
##                    parent.right = e1.right
##                else:
##                    print "something is wrong here!"
##                    sys.exit()
##            else:   
##                print "A-(A or V) -- betaReductionByValueEtaToWeakNF"
##                # we have already replaced e1 by e1' and e2 by e2'!
##                return

    def betaReductionHybridApplicativeEtaToNF(self,parent):
        # print "hae: "+self.traverse()
        if self.typ == 'V':
            # print "V -- betaReductionHybridApplicativeEtaToNF"
            # x --ha--> x
            return 
        elif self.typ == 'L':
            # print "L -- betaReductionHybridApplicativeEtaToNF"
            #      e --ha--> e'
            # ----------------------
            # (λx.e) --ha--> (λx.e')
            x,e =  self.left.left, self.right
            e.betaReductionHybridApplicativeEtaToNF(self)
        elif self.typ == 'A':
            # print "A -- betaReductionHybridApplicativeEtaToNF"
            # e1 --bv--> (λx.e)  e2 --ha--> e2'  e[e2'/x] --ha--> e'
            # ------------------------------------------------------
            # (e1 e2) --ha--> e'
            e1, e2 = self.left, self.right
            print e1.traverse()
            print e2.traverse()
            print "test Eta-Case"
            # problematisch ist, das im Ausdruck ( (λY.F) Ycombinator )
            # beim Einsetzen des Ycombinators in F dieser bereits ausgewertet wird.
            # Die Idee ist nun, den Ycombinator in einen Eta-Ausdruck zu verpacken.
            # Handelt es sich um einen Eta-Ausdruck, so soll dieser nicht ausgewertet werden.
            # ( (λY.F) (λu.Ycombinator u))
            if(e1.typ=='L' and e2.typ == 'A' and e2.left.typ == 'L' and e2.right.typ == 'V' and \
                      e2.left.left.left == e2.right.left):
                # + ((λy.f) ((λx.e) x)) -->ha--> f[e/y]
                # - ((λx.e) x)) -->bv--> e' 
                #  if self == parent.left:
                #       parent.left = e1.right
                #  else:
                #       parent.right = e1.right
                e1.right.substitute(e2.left.right,e1.left.left,e1)
                if self == parent.left:
                    parent.left = e1.right
                elif self == parent.right:
                    parent.right = e1.right
                print "Eta-Case"
                
                
            
            else:    
                e1.betaReductionByValueToWeakNF(self)
                e2.betaReductionHybridApplicativeEtaToNF(self)
                e1, e2 = self.left, self.right
                if(e1.typ == 'L'):
                    # print "A-L -- betaReductionHybridApplicativeToNF"
                    x, e = e1.left.left, e1.right
                    e.substitute(e2,x,e1) # Ergebnis ist nun in e1.right
                    e1.right.betaReductionHybridApplicativeEtaToNF(e1)
                    if self == parent.left:
                        parent.left = e1.right
                    elif self == parent.right:
                        parent.right = e1.right
                else:
                    # print "A-(A or V) -- betaReductionHybridApplicativeToNF"
                    e1.betaReductionHybridApplicativeEtaToNF(self)
                
    
    def betaReductionLeftmostOutermost(self, parent): # Das ist NormalToNF
        if self.typ == 'A':
            t1,t2 = self.left, self.right
            if t1.typ == 'L':
                y,r = t1.left.left, t1.right
                # if True: # Outermost
                # ('A', t1=('L',('V',y),r), t2)
                print "substitute (no) "+r.traverse()+": ersetze "+y+" mit "+t2.traverse()
                r.substitute(t2, y, t1)
                if parent.left == self:
                    parent.left = t1.right
                else:
                    parent.right = t1.right
                return True
            else:
                result = t1.betaReductionLeftmostOutermost(self) # Leftmost
                if not result:
                    result = t2.betaReductionLeftmostOutermost(self)
                return result
        elif self.typ == 'L':
            return self.right.betaReductionLeftmostOutermost(self)
        else:
            return False # keine Ersetzung (Variable)

    def betaReductionNormalOrderToNF(self, parent): # Das ist fehlerhaft
        if self.typ == 'A':
            t1,t2 = self.left, self.right
            if t1.typ == 'L':
                y,r = t1.left.left, t1.right
                if not r.betaReductionNormalOrderToNF(self):
                # ('A', t1=('L',('V',y),r), t2)
                    print "substitute "+r.traverse()+": ersetze "+y+" mit "+t2.traverse()
                    r.substitute(t2, y, t1)
                    if parent.left == self:
                        parent.left = t1.right
                    else:
                        parent.right = t1.right
                    return True
                else:
                    return False
            else:
                result = t1.betaReductionNormalOrderToNF(self)
                if not result:
                    result = t2.betaReductionNormalOrderToNF(self)
                return result
        elif self.typ == 'L':
            return self.right.betaReductionNormalOrderToNF(self)
        else:
            return False # keine Ersetzung (Variable)

      
    def betaReduce(self, pause=False, order="HybridApplicativeToNF"):
        i=0
        parent = Node('A',self,None)
        br = None
        brneu = self.traverse()
        while brneu != br:
            br = brneu
            i+=1
            print "betaReduce "+str(i)+":\n"+br
            if order == "LeftmostOutermost":
                parent.left.betaReductionLeftmostOutermost(parent)
            elif order == "HybridApplicativeToNF":
                parent.left.betaReductionHybridApplicativeToNF(parent)
            elif order == "ByValueToWeakNF":
                parent.left.betaReductionByValueToWeakNF(parent)
            elif order == "NormalOrderToNF":
                parent.left.betaReductionByValueToWeakNF(parent)
            elif order =="HybridApplicativeEtaToNF":
                parent.left.betaReductionHybridApplicativeEtaToNF(parent)
            else:
                print "Unbekannte Reduction Strategie!"
            brneu = parent.left.traverse()
            if pause:
                sys.stdin.read(1)
        return parent.left
            
# Grammatik für Lambda-Terme

# Beispiel:        \x y z.F x y == (\x (\y (\z ( (F x) y) ) ) )
# alternative 1:                == <x <y <z ( (F x) y) > > >
# alternative 2:   λx y z.F x y == (λx (λy (λz ((F x) y))))
# 
# lambda ::= 'λ' | '\' | '#'
# Ls ::= V Ls | V
# L  ::= lambda Ls . E | lambda V E | '<' V E '>'
# T  ::= V | L | '(' E ')'
# E ::= T E | T

'''     

λx y z.E  wird zu

        L
       / \
      V   L
     /   / \
    x   V   L
       /   / \
      y   V   E
         /
        z
'''     

import sys

class Parser:

    def __init__(self,expr,debug=False):
        self.expression = expr
        self.index=0
        self.c =' '
        self.stack = []
        self.name=""
        self.debug = debug

    def saveState(p):
        return ( len(p.stack), p.c, p.index )

    def restoreState(p,tup):
        length, p.c, p.index = tup
        while len(p.stack) > length:
            p.stack.pop()

    def wait(p,s):
        if not p.debug:
            return
        print s
        # sys.stdin.read(1)
    
    def ws(p,obligative=False):
        if(obligative):
            if not p.c.isspace():
                return False;
        while p.c.isspace():
            p.ch()
        return True
      
    def ch(p):
        if p.index >= len(p.expression):
            p.c = '#' # end of string
        else:
            p.c = p.expression[p.index]
            p.index+=1
        return True
      
    def point(p):            return p.c == '.' and p.ch()   
    def lambdaChar(p):       return (p.c==u'λ' or p.c=='\\') and p.ch()            
    def parenLeft(p):        return p.c == '(' and p.ch()
    def parenRight(p):       return p.c == ')' and p.ch()
    def lambdaParenLeft(p):  return p.c == '<' and p.ch()
    def lambdaParenRight(p): return p.c == '>' and p.ch()  

    def V(p):   
        p.name = ""
        if not p.c.isalnum() or p.c == u'λ':
            return False
        while p.c.isalnum() and p.c != u'λ':
            p.name += p.c
            p.ch()
        p.stack.append(Node('V',p.name,None))
        p.wait("aus V mit "+p.name)
        return True
      
    def Vs(p):
        p.wait("in Vs")
        if p.V():
            node = Node('L',p.stack.pop(),None)
            lastnode = node
            topnode = node
            p.ws(True)
            while p.V():
                node.right = Node('L',p.stack.pop(),None)
                lastnode = node.right
                node = node.right
                p.ws(True)
            p.stack.append(topnode)
            p.stack.append(lastnode)
            return True
        else:
            return False
  
    def L(p):
        p.wait("In L")
        result = False
        if p.lambdaChar() and p.ws():
            state = p.saveState()
            if p.Vs() and p.point():
                if p.ws() and p.E():
                    E = p.stack.pop()
                    last = p.stack.pop()
                    last.right = E # Die Vs sind noch und bleiben auf dem Stack
                    result = True
            else:
                p.restoreState(state)
                if p.V() and p.E():
                    E = p.stack.pop()
                    V = p.stack.pop()
                    p.stack.append(Node('L', V, E))
                    result = True
                else:
                    # print p.expression[:p.index]+"< hier folgt kein Lambda-Ausdruck >"+p.expression[p.index:]
                    result = False
        else:
            if p.lambdaParenLeft():
                if p.ws() and p.V() and p.E() and p.lambdaParenRight():
                    E = p.stack.pop()
                    V = p.stack.pop()
                    p.stack.append(Node('L', V, E))
                    result = True
            else:
                # print p.expression[:p.index]+"< hier folgt kein Lambda-Ausdruck >"+p.expression[p.index:]
                result = False
        p.wait("aus L mit "+str(result))
        return result

#    v w x y ==> (((v w) x) y)
#
#               A
#              / \
#             A   y
#            / \
#           A   x
#          / \
#         v   w
#
    def T(p):
         p.ws()
         if p.parenLeft():
            result = p.E() and p.parenRight()
         else:
            result = p.V() or p.L()            
         # result = p.parenLeft() and p.E() and p.parenRight() or p.V() or p.L()         
         if result:
             p.ws()
         return result
            
    def E(p):
        start = p.index
        p.wait("in E: "+p.expression[:p.index])
        result = False
        if p.T():
            nodeleft = p.stack.pop() # V | L | '(' E ')'    
            while p.T():                  
                nodeleft = Node('A',nodeleft,p.stack.pop())
            p.stack.append(nodeleft)
            result = True
        else:
            result = False
        p.wait("Aus E mit "+p.expression[start:p.index]+" "+str(result))
        return result

    def parse(p):
        if p.E():
            result = p.stack.pop()
        else:
            result = None
        return result


##Some Info from Peter Sestoft:
##
##>I am trying to understand the lambda calculus and get it 'running‘. I
##>have written a parser and a reducer (in python) that can perform normal
##>order reduction. There are more than thousand steps for the lambda
##>epression ‚Y F three’, likely as in your implementation. No I came across
##>your site and papers and read about all the other reduction strategies. I
##>am excited about the "hybrid applicative order“ and tried the expressions
##>in the next lines in the "Lambda calculus reduction workbench":
##>  
##>(\Z. Z F three) ( \f. (\x. ( x x ) ) (\x. ( f (\y. ((x x) y) ) ) ) )
##>
##>(\Z.( (Z F) three)) ((\x. \y. (y (\z. x x y z))) (\x. \y. (y (\z. x x y
##>z))))
##>
##>((Yv F) three)
##>
##>Guess what? All expression evaluate to "\f.\x.f (f (f (f (f (f (x))))))“
##>with normal order reduction, but don’t terminate with "hybrid applicative
##>order“ reduction. The worbench shows the following message:
##>
##>"
##>Hybrid applicative order:
##>
##>ERROR: Exceeded maximal step count: 4000
##
##I think the problem may be that when you use the call-by-value version Yv
##of the recursion combinator, you also need to write the function argument
##in a slightly different way, so use
##
##Yv Fv three
##
##instead of
##
##Yv F three
##
##where Fv = \f.\n.$iszero n (\d.$one) (\d.$mul n (f ($pred n))) (\d.d)
##and F = \f.\n.$iszero n $one ($mul n (f ($pred n)))
##
##Basically you need to delay the evaluation of the "branches" of choice
##operations such as $iszero = \n.n (\v.\x.\y.y) (\x.\y.x)
##
##In that case, hybrid applicative order reduction of (Yv Fv three)
##terminates in 180 beta-steps, where normal order requires more than 1500
##beta-steps.
##
##I hope this helps; otherwise get back to me!
##
##Peter
##
