#!/usr/bin/python
import numpy as np
import pandas as pd
from sklearn import feature_extraction
#from sklearn import metrics
#from sklearn import feature_selection
import SharedLibrary

## Convert numeric values to an string with an "S" suffix.
## Required for vec.fit_transform which will not split numeric features, even if strings.
def _ConvertToString(value):
    if (isinstance(value, basestring)):
        return value
    return str(value) + 'S'

## Convert a list of categorical features "cols" in to a separate 0./1. feature for each value.
## If replace = True remove the "col" from the "dataFrame".
## Used to improve performance in some models and to determine importance of values of features.
## cols = list of column names. Example: ['Pclass', 'Embarked', 'SalutationHash']
def OneHotDataframe(dataFrame, cols, replace=False):
    vec = feature_extraction.DictVectorizer(sparse=True)
    dataFrameCols = dataFrame[cols].astype(object) #  or DataFrame Pclass 3 1 3, ...
    cols_as_listOfdicts = []
    for i, row_i in dataFrameCols.iterrows():
        for colIndex in range(len(cols)):
            row_i[colIndex] = _ConvertToString(row_i[colIndex])
        
        cols_as_listOfdicts.append(dict(row_i.iteritems()))

    cols_as_arrayOfLists = vec.fit_transform(cols_as_listOfdicts).toarray() # array([[0., 0., 0., 1.], [0., 0., 1., 0.], ...] or array([[3.], [1.], [3.], ...}
    vecData = pd.DataFrame(cols_as_arrayOfLists)
    vecData.columns = vec.get_feature_names() # ['Embarked', 'Embarked=C', 'Embarked=S' ... ]
    vecData.index = dataFrame.index

    if replace:
        dataFrame = dataFrame.drop(cols, axis=1)
        dataFrame = dataFrame.join(vecData)
    return (dataFrame, vecData)
