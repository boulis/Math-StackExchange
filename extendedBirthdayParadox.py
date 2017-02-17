from math import factorial as fac
import random

def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom


# Code written to answer this question: 
# http://math.stackexchange.com/questions/2075874/how-much-data-needed-to-test-my-hypothesis#comment4274781_2075874


def recursiveSum(lowerlimit, upperlimit, level, N):
    if level == 0: return 1
    if level == 1: 
        # Sum {i=lower..upper}{i/N}    this is a simple arithmetic sequence multiplied by 1/N
        # formula given/verified by WolframAlpha http://www.wolframalpha.com/input/?i=sum%7Bi%3Dx,y%7D+i%2FN
        return (upperlimit+1 - lowerlimit)*(upperlimit+lowerlimit)/(2.0*N)

    return sum([i/float(N) * recursiveSum(i, upperlimit, level-1, N) for i in range(lowerlimit, upperlimit+1)])


N = 365 # the choices we have
m = 23  # the samples we take 

#N = pow(2,31)
#m = pow(2,18)

counts = [0]*40  # a array of buckets to keep counts of matches. Limit it from 0 to 19 matches



# theoretically calculate probability to to get exactly m matches
theory = True
if theory:
    print '--- THEORETICAL RESULTS ---'
    for matches in xrange(5):
        prob = fac(N)/fac(N-m+matches)/float(pow(N,m-matches)) * recursiveSum(1, m-matches, matches, N)
        print 'Probability of exactly', matches, 'matches is', prob 


# theoretically calculate probability to to get m OR LESS matches
theory2 = True
if theory2:
    print '--- THEORETICAL RESULTS 2 ---'
    prevProb = 0
    for matches in xrange(10):
        prob = 1
        for i in xrange(1, m-matches):
            prob *= (N-i)/float(N)
        #prob *= binomial(m-1, matches)
        print 'Probability of getting', matches, 'matches or less is', prob, '   Exactly these matches:',  prob - prevProb
        prevProb = prob


# Calculate the probability by simulation
simulation = False
if simulation:
    print '--- SIMULATION RESULTS ---'
    runs = 1000
    bingo = 0
    for r in xrange(runs):
        # take m random samples. Remove the matches/dublicates by taking the set, and then get the length of the set.
        # (m - the length of the set) is the number of matches we had
        matches = m - len(set([random.randint(1,N) for i in xrange(m)]))
        # increment the corresponding count bucket
        counts[matches] +=1

    
    for i, c in enumerate(counts):
        print 'Times we got', i, 'matches:', c, "  Rate = ",  float(c)/runs