print(__doc__)

# ---------
import sys
import os

COMMON_DIR = os.path.abspath(__file__ + '/../../common/')

sys.path.insert(0, COMMON_DIR)
from constants import *

sys.path.insert(0, UTILS_DIR)
from file_utils import *
# ---------


# Code source: Gael Varoqueux
# Modified for Documentation merge by Jaques Grobler
# License: BSD 3 clause

import numpy as np
import pylab as pl
from sklearn import linear_model, datasets


lines = read_to_lines('/home/manish/Dropbox/Thesis/MGSeCor/result/cve_cve/cross_site_scripting/from85_result.data', False)
results = []
for line in lines:
	result = line.split(',')
	result = [float(x.strip()) for x in result]
	results.append(result)


# import some data to play with
#iris = datasets.load_iris()
#X = iris.data[:, :2]  # we only take the first two features.
#Y = iris.target

X = np.array([x[0:2] for x in results][0:75])
Y = np.array([x[2] for x in results][0:75])

X_test = np.array([x[0:2] for x in results][75:])
Y_test = np.array([x[2] for x in results][75:])

h = .02  # step size in the mesh

logreg = linear_model.LogisticRegression(C=1e5)

# we create an instance of Neighbours Classifier and fit the data.
logreg.fit(X, Y)
print '**************************'
print 'Weight Vector'
print logreg.coef_
print '**************************'
print 'Actual:     ', ['%.2f' % z for z in Y_test.tolist()]

error = 0
errors = []
for i in range(len(Y_test.tolist())):
	error = error + ((Y_test.tolist()[i]-logreg.predict(X_test).tolist()[i])**2)
	errors.append((Y_test.tolist()[i]-logreg.predict(X_test).tolist()[i])**2),
print list(sorted(errors))
print 'Combination:', ['%.2f' % z for z in logreg.predict(X_test).tolist()], (error/len(Y_test.tolist()))**0.5

error = 0
for i in range(len(Y_test.tolist())):
	error = error + ((Y_test.tolist()[i]-[x[0] for x in results][75:][i])**2)
print 'Secure:     ', ['%.2f' % z for z in [x[0] for x in results][75:]], (error/len(Y_test.tolist()))**0.5

error = 0
for i in range(len(Y_test.tolist())):
	error = error + ((Y_test.tolist()[i]-[x[1] for x in results][75:][i])**2)
print 'Generic:    ', ['%.2f' % z for z in [x[1] for x in results][75:]], (error/len(Y_test.tolist()))**0.5
print '**************************'
"""
# Plot the decision boundary. For that, we will assign a color to each
# point in the mesh [x_min, m_max]x[y_min, y_max].
x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
pl.figure(1, figsize=(4, 3))
pl.pcolormesh(xx, yy, Z, cmap=pl.cm.Paired)

# Plot also the training points
pl.scatter(X[:, 0], X[:, 1], c=Y, edgecolors='k', cmap=pl.cm.Paired)
pl.xlabel('Sepal length')
pl.ylabel('Sepal width')

pl.xlim(xx.min(), xx.max())
pl.ylim(yy.min(), yy.max())
pl.xticks(())
pl.yticks(())

pl.show()
"""
