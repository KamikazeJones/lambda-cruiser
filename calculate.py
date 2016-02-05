#!/usr/bin/python
# -*- coding: utf-8 -*-

from parser2 import Parser
import sys
import codecs
print sys.platform

if sys.platform=="win32":
	codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
	reload(sys)
	sys.setdefaultencoding('utf-8')

##if sys.platform =="darwin":
##        reload(sys)
##        sys.setdefaultencoding('utf-8')
##        
def writeln(s):
	s.encode("utf-8")

#n1 = Node('L',Node('V','x',None),None)
#n1.right=Node('A',Node('V','x',None),Node('V','y',None))
#print n1.traverse()

expr  = u"λx y.(λa b.x a y b x z t)"
expr1 = "(x y)"
expr2 = u"(λc t)"
expr3 = "<x <t <e (x t)>>>"
expr4 = u"(λx (λy (λz ((F x) y))))"
expr5 = r"(\x (\y ((F y) x)))"

if False:
  p = Parser(expr3,True)
  e = p.parse()
      
  p2 = Parser(expr2)
  e2 = p2.parse()
  if e and e2:
      print e.traverse()
      print e.FV()
      print e2.traverse()
      e.right.substitute(e2,"x",e)
      print e.traverse()
  else:
      print "Fehler beim Parsen!"

  print e.FV() 

# Some Definitions from Dana Scott

O	= u"( λf x. x )"
I	= u"( λf x. f x )"
ZWEI    = u"( λf x. f (f x) )"
DREI    = u"( λf x. f (f (f x)) )"
pair    = u"( λx y pair. pair x y )"
first   = u"( λp. p (λx y. x) )"
second  = u"( λp. p (λx y. y) )"
succ    = u"( λn f x. f ( n(f) (x)) )"
shift   = u"( λs p. pair ( s (first p)) (first p) )"
# shiftlist = u"( λp.( pair ( succ (first p)) p ) )"
# pairlist = u"( λn cons zero. (n (shiftlist ) ( pair I zero) ) )"
pred    = u"( λn. second (n (shift succ) ( pair O O ) ) )"
test    = u"( λn u v.second ( n (shift λx.x) (pair (v) (u))) )"
plus    = u"(λm n f x. m f (n f x) )"
mult    = u"( λn m f. n (m f) )"
fold    = u"( λn g o. n g o) "    
F       = u"( λf n. test n  I ( mult n ( f (pred n) ) ) )"
# F       = u"( λf n. test n  I ( f (pred n) ) )" # hiermit funktioniert es schon!
##where Fv = \f.\n.$iszero n (\d.$one) (\d.$mul n (f ($pred n))) (\d.d)
Fv      = u"(λf n.test n (λd. I) (λd. mult n (f (pred n))) (λd.d))"
Y       = u"( λf. ( λx. f (x x ) ) λx. f (x x ) )" 
# Y       = u"( λf. (λx. (x x) ) λg. (f λx. (g x) (g x) ) )" 
# 
# liste: λ f x. shiftlist succ action ( shiftlist succ action ( shiftlist succ action x ) )


#  Y F von Hand reduzieren:
# ( λf. ( λx. f (x x ) ) λx. f (x x ) ) F == ( λx. F (x x ) ) λx. F (x x ) == F ( λx. F (x x )) (λx. F (x x )))

Z       = u"( λf. (λx.f (λv.((x x) v))) (λx.f (λv.((x x) v))))"
# Yv = \h.(\x.\a.h (x x) a) (\x.\a.h (x x) a)

Yv = u"(λh. ( (λx. (λa. ((h (x x)) a))) (λx. (λa. ((h (x x)) a)))))"
# Yv      = u"( λrec.( (λh.(h h)) (λg.(rec (λx.(( g g) x)))) ) )"
# Yv      = u"( λh.( (λrec.(rec rec)) (λx. (λa. ((h (x x)) a)))))"
# alle drei Yv Definitionen sind offenbar äquivalent

#(lambda (rec)
#      ( (lambda (h) (h h))  
#        (lambda (g)
#          (rec (lambda (x) ((g g) x))))))  
        
fact    = u"(Y F)"

expr1 = u"( (λ true false if. if true false true) <t<e t>> <t<e e>> λb then else.b then else )"
plusexpr = u"(λplus zwei drei. plus zwei drei)" \
          u"(λm n f x. m f (n f x) )" \
          u"(λf x. (f (f x)))" \
          u"(λf x. (f (f (f x))))"   
expr = u"<t <e t>> λt e f"
expr = u"λtλe t"

expr  = u"( (λ O I ZWEI DREI pair first second succ mult plus Y. (λ shift. (λ pred test. (λ F. (λ fact. fact DREI) "
expr  = u"( (λ O I ZWEI DREI pair first second succ mult Y. (λ shift. (λ pred test. (λ F. (λ fact. fact DREI) "

# Teste mit Fv, Yv
F = Fv
Y = Yv
Y = u"( (λd."+Yv+") d)"

expr += fact +") " + F +") " + pred + test + ")" + shift +")"
expr += O + I + ZWEI + DREI + pair + first + second + succ + mult + Y + ")"

tshift = u"( λs p. "+pair+" ( s ( "+first+" p)) ( "+first+" p) )"
tpred  = u"( λn. "+second+" (n ( "+tshift+" "+ succ+" ) ( "+pair +" "+O+" "+ O+" ) ) )"
ttest  = u"( λn u v. "+second+" ( n ( "+tshift+u" λx.x) ( "+pair+" (v) (u))) )"
tFv    = u"(λf n."+ttest+u" n (λd. "+I+u" ) (λd. "+mult+" n (f ("+tpred+u" n))) (λd.d))"
tF     = u"( λf n. "+ttest+" n "+ I+" ( "+mult+" n ( f ("+tpred+" n) ) ) )"

tfact  = u"("+Yv+" "+tFv+" "+DREI+" "+")"

dYv     = u"(λd.("+Yv+u" d) )"
tfact2  = u"( λc.( ( λdYv.dYv c"+tFv+" "+DREI+" "+")"+dYv+u" ) λd.d)"
tfact3  = u"( ( λF DREI."+Yv +" F DREI)"+ tFv +" "+DREI+")"


# expr  = u"(λ O I ZWEI DREI pair first second succ mult plus."
# expr += u"(λ shift shiftlist. (λ pred test pairlist. "

# expr += u"(λfoldr. " 

# Wie sieht denn eine pair-Liste aus?
# λ pair . (pair e1 ( pair e2 ( pair e3 ( pair O O ) ) ) )
#foldif = u"(λf z e. test e (λx y.z) f)"
# foldr = u"(λpl f z.( pl f z ))"

# expr += u"(λL. foldr L plus O) ((λ pair zero. (pair DREI ( pair ZWEI ( pair I ( zero ) ) ) ) ) )"
#expr += u"( (λcons ZERO. pairlist DREI cons ZERO) )"


# expr += ") "  + foldr
# expr += ") "  + pred + test + pairlist + ")"
# expr += shift + shiftlist + ")" + O + I + ZWEI + DREI + pair + first + second + succ + mult + plus +")"

# print u"λtλe t"
# print expr

tY2  = u"( ( λY. Y "+tFv+" "+DREI+" "+")"+u"( (λd."+Yv+") d) )"
tY3  = u"( ( λY. Y "+tFv+" "+DREI+" "+")"+Yv+")" 
tY1  = u"( (λd.f) d) )"
# (e1 e2) --> ((Yv tFv) DREI)

def calculate(expr,strategy="LeftmostOutermost"):
    print "Verwende als Reduction-Strategie: "+strategy
    p = Parser(expr)
    e = p.parse()
    if e:
        print e.traverse()
        # result = e.betaReduce(pause=False,order="LeftmostOutermost")
        result = e.betaReduce(pause=False,order=strategy)
        # result = e.betaReduce(pause=False,order="HybridApplicative")
        print "\nErgebnis: \n"+result.traverse()
    else:
        print "Fehler beim Parsen!"


# calculate(tfact3,"HybridApplicativeToNF")
calculate(expr,"HybridApplicativeEtaToNF")
# calculate(expr)
