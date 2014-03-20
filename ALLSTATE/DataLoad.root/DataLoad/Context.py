class Context(object):
    """
    Program context used to encapulate configuration paramater passing.
    """
    def __init__(self): 
        self.__trainCsvUNC = "D:/DEV_2012/KAGGLE/ALLSTATE/DATA/Train_01_Small.csv" # Must use / not \
        self.__crossCsvUNC = "" # Must use / not \ if "" use validationPct on a random selection of trainCsvUNC
        self.__testCsvUNC = "D:/DEV_2012/KAGGLE/ALLSTATE/DATA/Test_01_Small.csv" # Must use / not \ if "" use validationPct on a random selection of trainCsvUNC
        self.__predictionCsvUNC = "D:/DEV_2012/KAGGLE/ALLSTATE/DATA/Prediction.csv" # Must use / not \
        self.__mssqlInstance = 'Trevor-PC'
        self.__mssqlDatabase = 'ALLSTATE'
        self.__mssqlUser = 'sa'
        self.__mssqlPassword = 'sa123'
        self.__ssasInstance = 'Trevor-PC'

    @property
    def TrainCsvUNC(self):
        return self.__trainCsvUNC

    @property
    def CrossCsvUNC(self):
        return self.__crossCsvUNC

    @property
    def TestCsvUNC(self):
        return self.__testCsvUNC

    @property
    def PredictionCsvUNC(self):
        return self.__predictionCsvUNC

    @property
    def FileCsvUNC(self):
        return self.__fileCsvUNC

    @property
    def MssqlInstance(self):
        return self.__mssqlInstance

    @property
    def MssqlDatabase(self):
        return self.__mssqlDatabase

    @property
    def MssqlUser(self):
        return self.__mssqlUser

    @property
    def MssqlPassword(self):
        return self.__mssqlPassword

    @property
    def SsasInstance(self):
        return self.__ssasInstance



