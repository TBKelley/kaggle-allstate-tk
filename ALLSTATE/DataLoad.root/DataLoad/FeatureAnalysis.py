import numpy as np
from pylab import *

def Sort(featureImportanceHistogram):
    temp = featureImportanceHistogram.view(np.ndarray)
    featureImportanceHistogram = temp[np.lexsort((temp[:, 0], ))]
    return featureImportanceHistogram

def Execute(modelName, featureImportanceHistogram):
    featureImportanceHistogram = Sort(featureImportanceHistogram)
    importance = featureImportanceHistogram[0::, 0].astype(np.float)
    features = featureImportanceHistogram[0::, 1]

    N = len(features)
    pos = arange(N)+0.5

    m = importance.tolist()
    barh(pos, m, align='center', color='#B8FF5C')

    f = features.tolist()
    yticks(pos, f)
    ylabel('Feature')
    xlabel('Importance')
    title('Feature Importance - ' + modelName)
    grid(True)
    show()
