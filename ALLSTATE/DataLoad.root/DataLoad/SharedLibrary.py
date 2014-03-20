import datetime
import copy
import re
import numpy as np
import scipy as sp
from sklearn import cross_validation

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

#Convert a probability to a prediction (0.0 or 1.0)
def ToPrediction(probablity):
    return 1.0 if probablity >= 0.5 else 0.0

# Score function
# Percent correct = RMSE = sum[(actual-pred)**2]/len(actual)
# actual = np.array()
# predicted = np.array()
def ScoreProb(actual, predicted):
    #e = [i - j for i, j in zip(actual, predicted)]
    #e2 = map(lambda x: x*x, e)
    #s = sum(e2)
    #score1= s/(1.0*len(actual))
    score = sum(map(lambda x: x*x, [i - j for i, j in zip(actual, predicted)]))/(1.0*len(actual))
    return score

# Score function
# convert actual, predicted to boolean first
# Percent correct = RMSE = sum[(actual-pred)**2]/len(act)
# actual = np.array()
# predicted = np.array()
def ScoreBolean(actual, predicted):
    #a = map(lambda x: x >= 0.5, actual)
    #p = map(lambda x: x >= 0.5, predicted)

    #e = [i - j for i, j in zip(a, p)]
    #e2 = map(lambda x: x*x, e)
    #s = sum(e2)
    #score1= s/(1.0*len(actual))
    score = sum(map(lambda x: x*x, [i - j for i, j in zip(map(lambda x: x >= 0.5, actual), map(lambda x: x >= 0.5, predicted))]))/(1.0*len(actual))
    return score

def TrainingError(dataType, modelName, clf, model, dfX, dfY):
    print dataType + ' error - ' + modelName

    print 'Full ' + dataType + ' Score = ' + str(clf.score(dfX, dfY)) + ' Accuracy' # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct

    try:
        probas = model.predict_proba(dfX)
        scoreBolean = ScoreBolean(dfY.tolist(), [x[1] for x in probas])
        scoreProb = ScoreProb(dfY.tolist(), [x[1] for x in probas])
        if (hasattr(clf, 'oob_score_')):
            print 'Full ' + dataType + ' Score = ' + str(clf.oob_score_) + ' Accuracy OOB' # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
        print 'Full ' + dataType + ' Cost  = ' + str(scoreBolean) + ' ScoreBolean'
        print 'Full ' + dataType + ' Cost  = ' + str(scoreProb) + ' ScoreProb'
    except AttributeError:
        # Method does not exist. Ignore
        pass

    print ''

# WARNING: Will effect modeles derived from clf
def CrossValidation(modelName, clf, dfX, dfY, n_fold=5):
    print 'Cross Validation error estimates n_fold=' + str(n_fold) + ' - ' + modelName
    clf = copy.deepcopy(clf)
    #Simple K-Fold cross validation. 5 folds.
    cv = cross_validation.KFold(len(dfX), n_folds=n_fold, indices=False)

    #iterate through the training and test cross validation segments and
    #run the classifier on each one, aggregating the results into a list
    resultsClfScore = []
    resultsScoreBolean = []
    resultsScoreProb = []
    for trainCv, testCv in cv:
        model = clf.fit(dfX[trainCv], dfY[trainCv])

        resultsClfScore.append(model.score(dfX[trainCv], dfY[trainCv]))

        try:
            probas = model.predict_proba(dfX[testCv])
            resultsScoreBolean.append(ScoreBolean(dfY[testCv].tolist(), [x[1] for x in probas]))
            resultsScoreProb.append(ScoreProb(dfY[testCv].tolist(), [x[1] for x in probas]))
        except AttributeError:
            pass ## Ignore

    # print out the mean of the cross-validated results
    print 'Average CV Score  = ' + str(np.array(resultsClfScore).mean()) + ' Accuracy'
    if (len(resultsScoreBolean) > 0):
        print 'Average CV Cost   = ' + str(np.array(resultsScoreBolean).mean()) + ' RMSE(ScoreBolean)'

    if (len(resultsScoreProb) > 0):
        print 'Average CV Cost   = ' + str(np.array(resultsScoreProb).mean()) + ' RMSE(ScoreProb)'

    print ''
