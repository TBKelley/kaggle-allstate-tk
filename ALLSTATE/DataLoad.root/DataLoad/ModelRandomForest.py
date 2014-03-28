#!/usr/bin/python
import pymssql
import numpy as np
import ast
from ConnectionSQL import ConnectionSQL
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import cross_validation
from sklearn.externals import joblib # Used to persist trained classifier to disk
import random
import PreProcessing
from OptimiseModelParameters import OptimiseModelParameters
import SharedLibrary
import Context
# Caclaulate Optimal Paramater Selection
# dataDict = {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}
# returns (estimators, max_features, max_depth, min_samples_split, min_samples_leaf)
# accuracy=0.804306220096 estimators=10 max_features=6 max_depth=4 min_samples_split=7 min_samples_leaf=2
# accuracy=0.804784688995 bootstrap=True min_samples_leaf=4 n_estimators= 75 max_features=12 min_samples_split=4 max_depth=5
# accuracy=0.806698564593 bootstrap=True min_samples_leaf=4 n_estimators=100 max_features=12 min_samples_split=7 max_depth=5
# accuracy=0.808612440191 bootstrap=True min_samples_leaf=3 n_estimators=30 max_features=6 min_samples_split=4 max_depth=8
# accuracy=0.810526315789 bootstrap=True min_samples_leaf=5 n_estimators=100 max_features=6 min_samples_split=4 max_depth=7
# accuracy=0.811004784689 bootstrap=True min_samples_leaf=3 n_estimators=30 max_features=12 min_samples_split=6 max_depth=6
# accuracy=0.813397129187 bootstrap=True min_samples_leaf=5 n_estimators=50 max_features=11 min_samples_split=4 max_depth=8
# accuracy=0.813397129187 bootstrap=True min_samples_leaf=2 n_estimators=50 max_features=10 min_samples_split=7 max_depth=9
# accuracy=0.815789473684 bootstrap=True min_samples_leaf=4 n_estimators=30 max_features=5 min_samples_split=6 max_depth=6
# accuracy=0.815789473684 bootstrap=False min_samples_leaf=2 n_estimators=20 max_features=13 min_samples_split=5 max_depth=5 (418, 44)
# accuracy=0.822966507177 bootstrap=False min_samples_leaf=4 n_estimators=50 max_features=5  min_samples_split=3 max_depth=10 (418, 42) Tied matches=0
# All following results are repeatable with random_state=1
# accuracy=0.811004784689 bootstrap=True min_samples_leaf=3 n_estimators=20 max_features=11 min_samples_split=5 max_depth=6  (418, 44) Tied matches=10
# accuracy=0.815789473684 bootstrap=True min_samples_leaf=2 n_estimators=20 max_features=14 min_samples_split=7 max_depth=9  (418, 42) Tied matches=1
# accuracy=0.818181818182 bootstrap=True min_samples_leaf=1 n_estimators=50 max_features=5  min_samples_split=6 max_depth=10 (418, 42) Tied matches=1

__modelName = 'RandomForest'
__featuresColumns = "Pclass, SexINT, SalutationHash, EmbarkedINT, AgeFLOAT, IsChild, IsAdult, HasFamily, HasParent, HasChild, HasSpouse, HasSibling, Parents, Children, Sibling, DeptCodeHash, DeckHash, DualOccupant, OtherSurvivers, HasOtherSurviver, OtherDied, HasOtherDied"
__optimiseParameters = False

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    # Default model parameter values
    n_estimators = 50
    max_features = 8 # None
    max_depth = 12
    min_samples_split=5
    min_samples_leaf=4
    bootstrap=False
    n_jobs=-1 # Avaiable CPUs
    random_state=1 # Use None or 0 to randomise results

    # model parameter ranges - used for searching for optimial parameter settings
    n_estimatorsList = [20, 30, 40, 50, 70, 80, 100, 110]
    max_featuresList = [7, 8, 9, 10, 11, 12, 13, 14, None]
    #max_featuresList = ['auto']
    max_depthList = [6, 8, 10, 11, 12, 13, 14]
    min_samples_splitList = [3, 5, 6, 7, 8, 9]
    min_samples_leafList = [3, 4, 5, 6, 7]
    bootstrapList = [False]
    parameterRangeDict = {'n_estimators':n_estimatorsList, 'max_features':max_featuresList, 'max_depth':max_depthList, 'min_samples_split':min_samples_splitList, 'min_samples_leaf':min_samples_leafList, 'bootstrap':bootstrapList }

    # 0=DataID, 1=Actual, 2=Pclass, ...
    # Load Training Data and Cross Validation Data
    train_X, train_Y, train_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Train", preProcessDataFrame=__PreProcessDataFrame)
    #train_DataID = None

    # Load Cross Validation Data
    cross_X, cross_Y, cross_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="Cross", preProcessDataFrame=__PreProcessDataFrame)
    #cross_DataID = None

    if (__optimiseParameters):
        # package paramaters
        dataDict = {'train_X':train_X, 'train_Y':train_Y, 'cross_X':cross_X, 'cross_Y':cross_Y}

        # Optimal Paramater selection
        #parameterDictMax = __OptimalParamaterSelection(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)
        optimiseModelParameters = OptimiseModelParameters(modelName=__modelName)
        optimiseModelParameters.Percent = 0.05 # 5%
        parameterDictMax, accuracyMax = optimiseModelParameters.ExecuteMoneCarlo(dataDict=dataDict, accuracyFunct=__Accuracy, parameterRangeDict=parameterRangeDict)

        bootstrap = parameterDictMax['bootstrap']
        min_samples_leaf = parameterDictMax['min_samples_leaf']
        n_estimators = parameterDictMax['n_estimators']
        max_features = parameterDictMax['max_features']
        min_samples_split = parameterDictMax['min_samples_split']
        max_depth = parameterDictMax['max_depth']

    print __modelName + ' bootstrap=' + str(bootstrap) + ' min_samples_leaf=' + str(min_samples_leaf) + ' n_estimators=' + str(n_estimators) + " max_features=" + str(max_features) + " min_samples_split=" + str(min_samples_split) + " max_depth=" + str(max_depth)
    oob_score = bootstrap  # Can only have oob_score if bootstrap = True
    clf = RandomForestClassifier(n_jobs=-1, oob_score=oob_score, random_state=1,
                                 bootstrap=bootstrap, min_samples_leaf=min_samples_leaf, n_estimators=n_estimators, max_features=max_features, min_samples_split=min_samples_split, max_depth=max_depth)
    model = clf.fit(train_X, train_Y) # All features must be float.
    print ''

    # Persist trained classifier to disk
    # clfUNC = __modelName + '.clf'
    #joblib.dump(clfUNC)
    #clf = joblib.load(clfUNC)

    # Training error reports
    SharedLibrary.TrainingError(dataType='Training', modelName=__modelName, clf=clf, model=model, dfX=train_X, dfY=train_Y)
    SharedLibrary.TrainingError(dataType='CrossVal', modelName=__modelName, clf=clf, model=model, dfX=cross_X, dfY=cross_Y)

    # Cross validation report
    SharedLibrary.CrossValidation(modelName=__modelName, clf=clf, dfX=train_X, dfY=train_Y, n_fold=5)

    # UPDATE DRV_Predict with all data predictions.
    all_X, all_Y, all_DataID = connectionSQL.GetFeaturesAndResults(featuresColumns=__featuresColumns, dataType="ALL", preProcessDataFrame=__PreProcessDataFrame)
    all_Y = None
    connectionSQL.Update_DRV_Predict(modelName=__modelName, model=model, all_X=all_X, all_DataID=all_DataID)

    # Feature analysis summary
    featureImportances = enumerate(clf.feature_importances_)
    featureImportanceHistogram = np.array([(importance,train_X.columns[i]) for (i,importance) in featureImportances if importance > 0.005])

    return __modelName, featureImportanceHistogram

def __PreProcessDataFrame(df):
    df['Sex'] = df.apply(lambda row: SharedLibrary.ToMF(row['SexINT']), axis=1)
    df = df.drop(['SexINT'], axis=1)

    df['Embarked'] = df.apply(lambda row: SharedLibrary.ToEmbarked(row['EmbarkedINT']), axis=1)
    df = df.drop(['EmbarkedINT'], axis=1)

    df['Deck'] = df.apply(lambda row: SharedLibrary.ToDeck(row['DeckHash']), axis=1)
    df = df.drop(['DeckHash'], axis=1)

    df['Salutation'] = df.apply(lambda row: SharedLibrary.ToSalutation(row['SalutationHash']), axis=1)
    df = df.drop(['SalutationHash'], axis=1)
    
    df = PreProcessing.OneHotDataframe(df, ['Sex', 'Embarked', 'Deck', 'Salutation'], replace=True)[0] # Convert canonical features to multiple binary features

    #df['DeptCode'] = df.apply(lambda row: SharedLibrary.ToDeptCode(row['DeptCodeHash']), axis=1)
    df = df.drop(['DeptCodeHash'], axis=1) # Suspected noise
    #df = PreProcessing.OneHotDataframe(df, ['DeptCode'], replace=True)[0] # Convert canonical features to multiple binary features

    #df['Pclass'] = df.apply(lambda row: SharedLibrary.To1st2nd3rd(row['Pclass']), axis=1)
    #df = PreProcessing.OneHotDataframe(df, ['Pclass'], replace=True)[0] # Convert canonical features to multiple binary features

    return df

# Calculate Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct
def __Accuracy(dataDict, parameterDict):
    train_X = dataDict['train_X']
    train_Y = dataDict['train_Y']
    cross_X = dataDict['cross_X']
    cross_Y = dataDict['cross_Y']

    bootstrap = parameterDict['bootstrap']
    min_samples_leaf = parameterDict['min_samples_leaf']
    n_estimators = parameterDict['n_estimators']
    max_features = parameterDict['max_features']
    min_samples_split = parameterDict['min_samples_split']
    max_depth = parameterDict['max_depth']

    oob_score = bootstrap

    clf = RandomForestClassifier(n_jobs=-1, oob_score=oob_score, random_state=1,
                                 bootstrap=bootstrap, min_samples_leaf=min_samples_leaf, n_estimators=n_estimators, max_features=max_features, min_samples_split=min_samples_split, max_depth=max_depth)
    model = clf.fit(train_X, train_Y) # All features must be float.
    accuracy = clf.score(cross_X, cross_Y) # Score=Accuracy=(TP+TN)/(TP+TN+FP+FN)=%Correct

    return accuracy

