import os
import datetime
import copy
import re
import numpy as np
import scipy as sp
from sklearn import cross_validation
from TimeStamp import TimeStamp

"""
Shared function library
"""

def SQL_Value(value):
    if (value is None or len(value) == 0 or value == "NULL" or value == "NA"):
        sqlValue = "NULL"
    else:
        sqlValue = "'" + str(value).replace("'", "''") + "'" # Handle escaping embedded in value

    return sqlValue

#Convert Sex(Gender) into an integer to feed
def SexINT(sex):
    if sex == 'female':
        sexINT = 1
    else:
        sexINT = 0
    return sexINT

def TrainingError(dataType, modelName, clf, model, dfX, dfY):
    timeStamp = TimeStamp('TrainingError-' + dataType + '-' + modelName)
    print dataType + ' error - ' + modelName
    print 'Full ' + dataType + ' Score = ' + str(clf.score(dfX, dfY)) + ' Accuracy' # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
    print 'Elaspe=' + timeStamp.Elaspse
    print ''

# WARNING: Will effect modeles derived from clf
def CrossValidation(modelName, clf, dfX, dfY, n_fold=5):
    timeStamp = TimeStamp('CrossValidation-' + modelName)
    print 'Cross Validation error estimates n_fold=' + str(n_fold) + ' - ' + modelName
    clf = copy.deepcopy(clf)
    #Simple K-Fold cross validation. 5 folds.
    cv = cross_validation.KFold(len(dfX), n_folds=n_fold, indices=False)

    #iterate through the training and test cross validation segments and
    #run the classifier on each one, aggregating the results into a list
    resultsClfScore = []
    for trainCv, testCv in cv:
        model = clf.fit(dfX[trainCv], dfY[trainCv])

        resultsClfScore.append(clf.score(dfX[trainCv], dfY[trainCv]))

    # print out the mean of the cross-validated results
    print 'Average CV Score  = ' + str(np.array(resultsClfScore).mean()) + ' Accuracy'
    print 'Elaspe=' + timeStamp.Elaspse
    print ''

# Find and remove files from a folder and 
# Usage:
#   path=os.path.join("/home","dir1","dir2")
#   FindAndRemove(path,".bak")
#   FindAndRemove("C:/DEV_2010/KAGGLE/ALLSTATE/DATA_Cache/",".tab")
def FindAndRemove(folderUNC, pattern, maxdepth=1):
    cpath=folderUNC.count("/")
    for rootUNC, subFolder, fileList in os.walk(folderUNC):
        if rootUNC.count("/") - cpath < maxdepth:
            for filename in fileList:
                if filename.endswith(pattern):
                    try:
                        #print "Removing %s" % (os.path.join(rootUNC, filename))
                        os.remove(os.path.join(rootUNC, filename))
                    except Exception,e:
                        print e
                    else:
                        print "%s removed" % (os.path.join(rootUNC, filename))

