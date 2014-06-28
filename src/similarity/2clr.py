
#! /usr/bin/python

import math
import random
import sys

max_exp = sys.float_info.max
min_exp = sys.float_info.min

train = []
test = []
eta = 0.01

def readfile():
	flag = 0
	f = open('/home/manish/Desktop/10-binary.data' , 'r')
	for line in f:
		#l = [1] + list(map(float, line.split(',')))
		l = [1] + [float(x.strip()) for x in line.split(',')]
		if (l[len(l) - 1] == 2):
			l[len(l) - 1] = 0
		train.append(l)
	f.close

def divide ():
	length = len(train)
	one_third = (int)(length / 3)
	for i in range(0, one_third):
		index = random.randint(0,len(train)-1)
		test.append(train[index])
		train.pop(index)
	print len(train), len(test)

def printinstances(l):
	for i in range (0, len(l) - 1):
		print l[i]

def w_dot_x(w, x):
	return sum(a*b for a,b in zip(w, x))

def is_equal(x, y):
	i = 0
	epsilon = [0.11, 0.11, 0.11, 0.11, 0.11]
	for a,b in zip(x, y):
		if (math.fabs(a - b) > epsilon[i]):
			return 0
		i += 1
	return 1

def find_w ():
	n = len(train[0]) - 1
	N = len(train)
	w = [0.0]*n
	count = 1
	g_old = [0.0]*n
	while 1 :
		g = [0.0]*n
		for i in range(0, N - 1):
			index = -1 * w_dot_x(w, train[i])
			if (min_exp <= index):
				p1 = 1
			else:
				if (index <= max_exp):
					p1 = 0
				else:
					p1 = 1 / (1 + math.exp(index))
			error = train[i][n] - p1
			# for j = 1 to n, gj = gj + errori * xij
			g = [a-b for a,b in zip(g, [error*x for x in train[i]])]
			#print "i = %s, p = %s, error = %s, g = %s" %(i, p, error, g)
			# w = w + eta * g
		eta_g = [eta*x for x in g]
		w_new = [a+b for a,b in zip(w, eta_g)]
		#print "\ncount = %s, g = %s, eta-g = %s, w_new = %s, w = %s\n" % (count, g, eta_g, w_new, w)
		#if (is_equal(w_new, w) or count > 10*N):
		#if (is_equal(w_new, w)):
		if (is_equal(g, g_old)):
			break
		g_old = g
		w = w_new   
		count += 1
	return w


def classify(w):
	N = len(test)
	n = len(test[0]) - 1
	accuracy = 0
	for i in range(N):
		if (w_dot_x(w, test[i]) > 0):
			label = 1
		else:
			label = 0

		print w_dot_x(w, test[i]), label, test[i][n]
		if (label == test[i][n]):
			accuracy += 1
		#print "%s, %s" % (test[i],label)
	print "Accuracy : %s, %s, %s" % (accuracy/(float)(N), accuracy, N)

def main():
	w = []
	readfile()
	divide()
	w = find_w()
	classify(w)
	print "Weight Vector : %s\n" % (w)

if __name__ == "__main__":
	main()
