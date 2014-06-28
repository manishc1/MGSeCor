"""
author  Ernesto Adorio, Ph.D.
		University of the Philippines 
		Extension Program in Pampanga.
		UPDEPP at Clarkfield, Pampanga 
 
email	ernesto.adorio@gmail.com
 
version 0.0.1- 2012.03.11   initial buggy implementation!
		0.0.2- 2012.03.15   fixing the gradient function. FAIL!
		0.0.3- 2012.03.15   basic routines only to compact the file.
"""
 
 
from math import exp, log
from scipy.optimize import fmin_bfgs
from numpy import array
 
def readcsv(filename, header=True, withintercept=True):
	try:
		data = open(filename, "r").read()
		data = data.replace(',', " ")
		data = data.strip()
		X = []
		Y = []
		colnames = None
		unnamed = True
		for i , line in enumerate(data.split("\n")):
			#print i + 1, line
			fields = line.split()
			if header and unnamed: 
				unnamed = False
				colnames = fields
				continue
			Y.append(int(fields[-1]*10))
			x =  [float(f) for f in fields[0:-1]]
			if withintercept:
				x.insert(0, 1.0)
			X.append(x)
		miny = min(Y)	
		if miny != 0:
			for i in range(len(Y)):
				Y[i] -= miny
		return X, Y, colnames
	except Exception as e:
		print str(e)
		return None, None, None
 
def itable(Y):
	"""
	Returns dictionary of unique elements.
	"""
	D={}
	for i, y in enumerate(Y):
		if y in D:
			D[y] += 1
		else:
			D[y] = 0
	return (D)
 
 
def negmloglik(Betas, X, Y,  m, reflevel=0):
	"""
	log likelihood for polytomous regression or mlogit.
	Betas - estimated coefficients, as a SINGLE array!
	Y values are coded from 0 to ncategories - 1
 
	Beta matrix
			b[0][0] + b[0][1]+ b[0][2]+ ... + b[[0][D-1]
			b[1][0] + b[1][1]+ b[1][2]+ ... + b[[1][D-1]
						...
			b[ncategories-1][0] + b[ncategories-1][1]+ b[ncategories-1][2]
			 .... + ... + b[[ncategories - 1][D-1]
 
			Stored in one array! The beta   coefficients for each level
			are stored with indices in range(level*D , level *D + D)
	X,Y   data X matrix and integer response Y vector with values 
			from 0 to maxlevel=ncategories-1
	m - number of categories in Y vector. each value of  ylevel in Y must be in the
			interval [0, ncategories) or 0 <= ylevel < m
	reflevel - reference level, default code: 0
	"""
 
	n  = len(X[0]) # number of coefficients per level.  
	L  = 0
	for row, (xrow, ylevel) in enumerate(zip(X,Y)):
		h   = [0.0] * m
		denom = 0.0
		for k in range(m):
				 if k == reflevel:
					h[k] = 0
					denom += 1
				 else:
					sa = k * n
					v = sum([(x * b) for (x,b) in zip(xrow, Betas[sa: sa + n])])
					h[k] = v
					denom += exp(v)
		deltaL = h[ylevel] - log(denom)
		L += deltaL		
	return -L
 
 
def gradnegmloglik(Betas, X, Y,  m, reflevel=0):
	"""
	The gradient of the log likelihood for polytomous regression or mlogit.
	See argument list in negmloglik.
	"""
 
	n	  = len(X[0]) # number of coefficients per level.  
	L	  = 0
	grad = array([0.0] * (m* n))
	for row, (xrow, ylevel) in enumerate(zip(X,Y)):
		h   = [0.0] * m
		denom = 0.0
		for k in range(m):
			 if k == reflevel:
				h[k] = 1
				denom += 1
			 else:
				sa = k * n
				v = sum([(x * b) for (x,b) in zip(xrow, Betas[sa: sa + n])])
				ev = exp(v)
				h[k] =ev
				denom += ev
		probij = [h[k] /denom for k in range(m)]
 
		for j in range(m):
			if j != reflevel:
				dij = 1 if (ylevel==j) else 0
				c	= dij - probij[j]
				for k in range(n):
					grad[j * n +k]  -=  c * xrow[k] 
	return array(grad)
 
 
def estmlogit(Betas, X,Y,  m=None, algo="bfgs", maxiter=50, epsilon = 1.0e-8, full_output=True, reflevel= 0, disp=False):
	"""
	Returns estimates of the unknown parameters of the multivalued logistic regression
		initial estimates, the response Y vector and predictors X matrix. X must have
	a column of all 1s if a constant is in the model! 
	The estimates are determined by fmin_bfgs.
	"""
 
	if m is None:
	   m = len(itable(Y))
 
	def floglik(betas):
		return negmloglik(betas, X, Y, m, reflevel=reflevel)
	def gfloglik(betas):
		return gradnegmloglik(betas, X, Y, m, reflevel=reflevel)	
 
	if algo=="bfgs":
	   output = fmin_bfgs(floglik , Betas, fprime=gfloglik, maxiter=maxiter, epsilon = epsilon, full_output = True, retall=False, disp=False)
	return output
 
 
if __name__=="__main__":
	X,Y, colnames = readcsv("/home/manish/Desktop/10-logit.data", False)
	print "Col Names=", colnames
	print "Y = ", Y
	ydict		   = itable(Y)
	m			   = len(ydict)
	n				= len(X[0])
 
	print "Testing negmloglik() function:"
	Betas=[				 0,			  0,			  0,
				  -11.774478, 0.523813, 0.368201,
				 -22.721201,  0.465939, 0.685902]
	Betas = array(Betas)
	print "Value of negmloglik from R: ",   -702.97
	print "Value of negmloglik from Py:", negmloglik(Betas, X, Y, m, reflevel=0)
	print "Gradient vector from Py:",	gradnegmloglik(Betas, X, Y, m, reflevel=0)	
	print "Running bfgs algorithm on negmloglik function:"
	Betas = array([0] * (m *n))	 
	output = estmlogit(Betas, X,Y,  m, reflevel= 0,algo="bfgs", maxiter=10,  full_output=True, disp=False)
	for field in output:
		print field
