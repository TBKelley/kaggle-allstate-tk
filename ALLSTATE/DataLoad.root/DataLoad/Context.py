class Context(object):
    """
    Program context used to encapulate configuration paramater passing.
    """
    def __init__(self):
        self.__reloadDatabase = False # Set to True to use cached %Type%_%Matrix%_%Model%.tab, will speed up debugging of model
        self.__trainCsv = "Train_00_Full.csv" # Must use / not \
        self.__crossCsvUNC = "" # Must use / not \ if "" use validationPct on a random selection of trainCsvUNC
        self.__testCsv = "Test_00_Full.csv" # Must use / not \ if "" use validationPct on a random selection of trainCsvUNC

        self.__cacheFolderUNC = "C:/DEV_2010/KAGGLE/ALLSTATE/DATA_Cache/" # Must use / not \
        self.__submissionFolderUNC = "C:/DEV_2010/KAGGLE/ALLSTATE/DATA_Submission/" # Must use / not \
        self.__dataFolderUNC = "C:/DEV_2010/KAGGLE/ALLSTATE/DATA/" # Must use / not \ location of Kaggle train, test .csv file
        self.__mssqlInstance = 'AU29543'
        self.__mssqlDatabase = 'ALLSTATE'
        self.__mssqlUser = 'sa'
        self.__mssqlPassword = 'sa123'
        self.__ssasInstance = 'AU29543\MULTIDIM'

    @property
    def ReloadDatabase(self):
        return self.__reloadDatabase

    @property
    def CacheFolderUNC(self):
        return self.__cacheFolderUNC

    @property
    def SubmissionFolderUNC(self):
        return self.__submissionFolderUNC

    @property
    def DataFolderUNC(self):
        return self.__dataFolderUNC

    @property
    def TrainCsvUNC(self):
        return self.DataFolderUNC + self.__trainCsv

    @property
    def CrossCsvUNC(self):
        return self.DataFolderUNC + self.__crossCsvUNC

    @property
    def TestCsvUNC(self):
        return self.DataFolderUNC + self.__testCsvUNC

    @property
    def PredictionCsvUNC(self):
        return self.__submissionFolderUNC + "Prediction.csv"

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




