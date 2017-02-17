from math import factorial as fac
import random


# Q: http://math.stackexchange.com/questions/2029575/what-are-the-odds-of-winning-this-bingo-game/ 


def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

def probMatchWithMultiCalls(N,k,m, level=0):
    padding = ' '*level
    if debug: print padding, N,k,m, 

    if m==1: 
        if debug: print "terminating answer:", 1 - (N-k)/float(N)
        return 1 - (N-k)/float(N)
    if k==m:
        if debug: print "terminating answer:", 1.0/binomial(N,k)
        return 1.0/binomial(N,k)
    
    if debug: print

    p = (N-m)/float(N)  # none of our m numbers match the first of k numbers called out 
    noSuccesCase = probMatchWithMultiCalls(N-1,k-1,m, level+1)
    SuccessCase = probMatchWithMultiCalls(N-1,k-1,m-1, level+1)
    
    if debug: print padding, 'Answer for', N,k,m, 'is',  p, '*', noSuccesCase, '+', 1-p, '*', SuccessCase, '=',  p * noSuccesCase + (1-p) * SuccessCase
    return p * noSuccesCase + (1-p) * SuccessCase


debug = False 
#debug= True
#N = 20; k = 6; m = 3
#N = 17; k = 3; m = 2
#N = 30; k = 10; m = 5
N = 75; k = 20; m = 8

result = probMatchWithMultiCalls(N,k,m)
print "Probability to match", m, "numbers with", k, "calls out of", N, "numbers (recursive calculation):", result

# answer provided here: http://math.stackexchange.com/questions/2029575/what-are-the-odds-of-winning-this-bingo-game/
exact = binomial(N-m, k-m)/float(binomial(N, k))
print "Probability to match", m, "numbers with", k, "calls out of", N, "numbers (closed form):", exact

# this is my way that I found afterwards. Even simpler!
exact = binomial(k, m)/float(binomial(N, m))  
print "Probability to match", m, "numbers with", k, "calls out of", N, "numbers (alt closed form):", exact

# Calculate the probability by simulation
simulation = False
if simulation:
    runs = 200000
    bingo = 0
    for r in xrange(runs):
        target = set(random.sample(range(N), m))
        callout = set(random.sample(range(N), k))
        if target.issubset(callout): bingo += 1

    print "Probability to match", m, "numbers with", k, "calls out of", N, "numbers (simulated):", float(bingo)/runs


# probability for exactly i matches in a row
total = 0
for i in range(m+1):
    p = binomial(m,i)* fac(N-k)/float(fac(N-k-m+i)) * fac(k)/float(fac(k-i)) * fac(N-m)/float(fac(N))
    print N,k,m,': prob for exactly', i, 'matches =', p
    total +=p
print 'Total (just to check) =', total


# probability for exactly i matches in a non-winning row (i.e we know matches are < m)
total = 0
print '\nGiven a non winning row we have:'
for i in range(m):
    p = binomial(m-1,i)* fac(N-1-k)/float(fac(N-1-k-(m-1)+i)) * fac(k)/float(fac(k-i)) * fac(N-1-(m-1))/float(fac(N-1))
    print N,k,m,': prob for exactly', i, 'matches =', p
    total +=p
print 'Total (just to check) =', total
