
# To answer math.stachexchange question:
# https://math.stackexchange.com/questions/2355852/bins-and-balls-problem-expected-number-of-balls-placed-given-number-of-empty-an/

import random
from math import factorial as fac

def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

bins = 10
balls = 20


# the following theoretical calculation is not correct, I was just experimenting. The correct formula is given in the answers.
print '------------ Theoretical ------------------'
total = 0
for empty_bins in xrange(bins-1,-1,-1):
	full_bins = bins - empty_bins
	prob = float(binomial(bins, empty_bins) * binomial(balls - full_bins + full_bins -1, full_bins-1)) / binomial(balls+ bins-1, bins-1)
	total += prob
	print 'Probability of', full_bins, 'non empty bins:', prob

print 'Sum of probabilities:', total


print '------------ Simulation ------------------'
runs = 1000000
counts = [0]*bins
for r in xrange(runs):
	non_empty_bins = len(set([random.randint(1,bins) for i in xrange(balls)]))
	counts[non_empty_bins -1] += 1

for i, c  in enumerate(counts):
	print 'Probability of', i+1, 'non empty bins:', float(c)/runs

print 'Sum of probabilities:', sum(counts)