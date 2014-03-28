import os.path
import csv as csv
import math
import numpy as np
import pymssql
import pandas as pd
import pandas.io.sql as sql
from sklearn import preprocessing
from TimeStamp import TimeStamp
import SharedLibrary
import Context

class ConnectionSQL(object):
    """
    Connection class used to encapulate SQL methods.
    """
    def __init__(self, context):
        self.__cacheFolderUNC = context.CacheFolderUNC
        self.__mssqlInstance = context.MssqlInstance
        self.__mssqlDatabase = context.MssqlDatabase
        self.__mssqlUser = context.MssqlUser
        self.__mssqlPassword = context.MssqlPassword
        self.__batch_size = 1000 # MSSQL Max is 1,000

    @property
    def CacheFolderUNC(self):
        return self.__cacheFolderUNC

    @property
    def MssqlInstance(self):
        return self.__mssqlInstance

    @property
    def MssqlDatabase(self):
        return self.__mssqlDatabase

    @property
    def BatchSize(self):
        return self.__batch_size

    # Set as_dict=True to return rows as Dictionary (not List) so column can be indexed by columnName
    def Connect(self, as_dict=False):
        conn = pymssql.connect(host=self.__mssqlInstance, user=self.__mssqlUser, password=self.__mssqlPassword, database=self.__mssqlDatabase, as_dict=as_dict)
        return conn

    def Cursor(self, conn):
        cur = conn.cursor()
        return cur

    def Execute(self, sql):
        conn = self.Connect()
        cur = self.Cursor(conn)
        print sql
        cur.execute(sql)
        conn.commit()
        conn.close()

    def ExecuteAuoCommit(self, sql):
        conn = self.Connect()
        conn.autocommit(True)
        cur = self.Cursor(conn)
        print sql
        cur.execute(sql)
        conn.autocommit(False)
        conn.close()

    # TRUNCATE MSSQL TableName, resetting any INT IDENTITY(Start,Increment)
    def TruncateTable(self, TableName):
        self.Execute("TRUNCATE TABLE " + TableName)

    # Execute SelectSql and return a list of first column values
    # SelectSql = list of values Example: 'SELECT [State] FROM [RAW_Data] GROUP BY [State] ORDER BY [State]' Only first column is added to list
    # Returns a list of values ['AL', 'AR', 'CO', 'CT', 'DC', 'DE', ...]
    def GetValueListFromSelect(self, SelectSql):      
        conn = self.Connect()
        cur = self.Cursor(conn)

        print SelectSql
        cur.execute(SelectSql)
        print 'FetchAll rows'
        rows = cur.fetchall() # Must cache all to avoid connection closing issues in execute(sql)
        print '  Rows read = ' + str(len(rows))
        conn.close()

        valueList = []
        for row in rows:
            valueList = valueList + [row[0]]

        print valueList
        return valueList

    # Execute SelectSql and retuen a list of row tuplets
    # Returns a list of row tuplets [(10, 3, 80, 0, 1.0), (11, 2, 82, 1, 2.0), ...]
    def GetRowsListFromSelect(self, SelectSql):      
        conn = self.Connect()
        cur = self.Cursor(conn)

        print SelectSql
        cur.execute(SelectSql)
        print 'FetchAll rows'
        rows = cur.fetchall() # Must cache all to avoid connection closing issues in execute(sql)
        print '  Rows read = ' + str(len(rows))
        conn.close()
        return rows

    # Execute SelectSql and return dictionary of rows.
    # Returns dictionary of SQL rows [{u'Actual':False, u'Age':22.0,u'Cabin':None,u'Embarked':u'S'}, ...]
    def GetRowsDictFromSelect(self, SelectSql):      
        conn = self.Connect(as_dict=True)
        cur = self.Cursor(conn)

        print SelectSql
        cur.execute(SelectSql)
        print 'FetchAll rows'
        rows = cur.fetchall() # Must cache all to avoid connection closing issues in execute(sql)
        print '  Rows read = ' + str(len(rows))
        conn.close()
        return rows

    # Execute SelectSql and return pandas DataFrame of rows.
    # Returns pandas DataFrame of SQL rows 
    def GetRowsDataFrameFromSelect(self, SelectSql):
        conn = self.Connect(as_dict=False)    
        print SelectSql
        df = sql.read_frame(SelectSql, conn)
        
        print '  Rows read = ' + str(df.shape[0])
        conn.close()
        return df

    # INSERT a CSV file to an MS SQL Table
    # TestCsvUNC   : UNC of the .csv table
    # DataType     : 0=Training, 1=Cross Validation, 3=Test
    # mssqlColumns : SQL Table columns names
    # mssqlTable   : SQL Table
    # NOTE: Records are INSERTed self.BatchSize at a time as MS SQL has a 1,000 record limit per transaction
    def RAW_Data_Load(self, TestCsvUNC, DataType, mssqlColumns):
        fileCsvUNC = TestCsvUNC
        mssqlTable = "[dbo].[RAW_Data]"
        insert_header = "INSERT " + mssqlTable + " (" + mssqlColumns + ") VALUES\n"
        conn = self.Connect()
        cur = self.Cursor(conn)
        timeStamp = TimeStamp()

        print 'Open ' + fileCsvUNC
        fileCsv = csv.reader(open(fileCsvUNC, 'rb'))
        header = fileCsv.next() # Skip first line, headers

        batch_size = self.BatchSize
        prefixRow = " "
        batch_counter = batch_size+1
        row_counter = 0
        sql = ""
        print 'INSERT batches of rows with batch size=' + str(batch_size)
        print insert_header
        for row in fileCsv:
            if (batch_counter >= batch_size):
                if (row_counter != 0):
                    print 'INSERT ' + mssqlTable + ' rows ' + str(row_counter+1-batch_counter) + ' to ' + str(row_counter)
                    try:
                        cur.execute(sql)
                        conn.commit()
                    except:
                        print 'SQL INSERT Error row_counter=' + str(row_counter)
                        print 'HINT: Set batch_size=1'
                        print sql
                        raise

                batch_counter = 0
                prefixRow = " "
                sql = ""
                sql += insert_header

            row_counter += 1
            batch_counter += 1
            prefixColumn = prefixRow + "(" + DataType + "," # DataType 3=Test
            prefixRow = ","
            for rowIndex, value in enumerate(row):
                columnValue = SharedLibrary.SQL_Value(value)
                sql += prefixColumn + columnValue
                prefixColumn = ","
            sql += ")\n"

        if (batch_counter != 0):
            print 'INSERT ' + mssqlTable + ' rows ' + str(row_counter+1-batch_counter) + ' to ' + str(row_counter)
            try:
                cur.execute(sql)
                conn.commit()
            except:
                print 'SQL INSERT Error row_counter=' + str(row_counter)
                print 'HINT: Set batch_size=1'
                print sql
                raise

        conn.close()

        print 'DONE... ' + str(row_counter) + ' rows inserted into [' + self.MssqlInstance + '].[' + self.MssqlDatabase + '].' + mssqlTable + ' Elaspe=' + timeStamp.Elaspse
        print ''

    # INSERT rows to an MSSQL table defined by RowHeader and rows formatted by FunctProcessRow
    # rows = List of lists [[Col1Value, Col2Value, ...] [Col1Value, Col2Value, ...]]
    # RowHeader = INSERT SQL. Example: "INSERT [dbo].[DRV_Predict] (Model, DataID, Predicted, Probablity) VALUES\n"
    # FunctProcessRow = Function used to format a single row without brackets. Example: "'Col1Value', Col2Value, 'Col3Value'"
    # paramDict = NOT USED!  Parameter dictionary {'modelName':'Base', 'model':clfModel}
    def Loop_INSERT(self, rows, RowHeader, FunctProcessRow, paramDict=None):
        conn = self.Connect()
        cur = self.Cursor(conn)
        timeStamp = TimeStamp()

        batch_size = self.BatchSize
        prefixRow = " "
        batch_counter = batch_size+1
        row_counter = 0
        sql = ""

        print RowHeader
        for row in rows:
            if (batch_counter >= batch_size):
                if (row_counter != 0):
                    print 'INSERT rows ' + str(row_counter+1-batch_counter) + ' to ' + str(row_counter)
                    try:
                        cur.execute(sql)
                        conn.commit()
                    except:
                        print 'SQL INSERT Error row_counter=' + str(row_counter)
                        print 'HINT: Set batch_size=1'
                        print sql
                        raise

                batch_counter = 0
                prefixRow = " "
                sql = ""
                sql += RowHeader

            row_counter += 1
            batch_counter += 1

            sql += prefixRow + "("
            sql += FunctProcessRow(row, paramDict) # row sql without '(' and ')'
            sql += ")\n"
            prefixRow = ","

        if (batch_counter != 0):
            print 'INSERT rows ' + str(row_counter+1-batch_counter) + ' to ' + str(row_counter)
            try:
                cur.execute(sql)
                conn.commit()
            except:
                print 'SQL INSERT Error row_counter=' + str(row_counter)
                print 'HINT: Set batch_size=1'
                print sql
                raise

        conn.close()
        print 'DONE... ' + str(row_counter) + ' rows inserted. Elaspe=' + timeStamp.Elaspse
        print ''


    # Generate SQL to insert a single row, without "(" and ")"
    def __DRV_PredictRow(self, row, paramDict):
        sql = ""

        modelName = paramDict['modelName']
        model = paramDict['model']

        DataID = row[0]
        Predicted = row[1]
        Probablity = row[2]

        sql += "'" + modelName + "'"
        sql += "," + str(DataID)
        sql += ",'" + Predicted + "'"
        sql += "," + str(Probablity)

        return sql

    # Upadte DRV_Predict with predictions of all data records (Training, CrossValidation, Test, Boost)
    # modelName = Example: 'DescisionTree' for ModelDescisionTree
    # model = Trained Classification Model, must support methods .predict(X) and .predict_proba(X)
    # all_X = Feature DataFrame for all data records
    # all_DataID = Series for all DataID matching all_X
    def Update_DRV_Predict(self, modelName, model, all_X, all_DataID):
        print 'Update [dbo].[DRV_Predict]'

        self.Execute("DELETE [dbo].[DRV_Predict] WHERE [Model] = '" + modelName + "'")

        rowHeader = "INSERT [dbo].[DRV_Predict] (Model, DataID, Predicted, Probablity) VALUES\n"
    
        predictAllList = model.predict(all_X) # predictAllList[row 0..n][PredictedLableValue0, PredictedLableValue1, ...] # Multiclass-multilable

        hasProbas = False
        try:
            if (hasattr(model, 'predict_proba')):
                #probasAllMatrix = model.predict_proba(all_X) # probasAllMatrix[class 0..6][row 0..n] [P(Lable0), P(Lable1), ...] # Multiclass-multilable
                probasLogAllMatrix = model.predict_log_proba(all_X) # probasAllMatrix[class 0..6][row 0..n] [P(Lable0), P(Lable1), ...] # Multiclass-multilable
                hasProbas = True
        except AttributeError:
            pass ## Ignore

        labelEncoderA = preprocessing.LabelEncoder()
        labelEncoderB = preprocessing.LabelEncoder()
        labelEncoderC = preprocessing.LabelEncoder()
        labelEncoderD = preprocessing.LabelEncoder()
        labelEncoderE = preprocessing.LabelEncoder()
        labelEncoderF = preprocessing.LabelEncoder()
        labelEncoderG = preprocessing.LabelEncoder()

        labelEncoderA.fit([0, 1, 2])
        labelEncoderB.fit([0, 1])
        labelEncoderC.fit([1, 2, 3, 4])
        labelEncoderD.fit([1, 2, 3])
        labelEncoderE.fit([0, 1])
        labelEncoderF.fit([0, 1, 2, 3])
        labelEncoderG.fit([1, 2, 3, 4])

        rows = []
        for rowIndex in range(len(predictAllList)):
            dataID = all_DataID['DataID'][rowIndex]
            predictedList = predictAllList[rowIndex]
            predicted = ''
            predicted += str(int(predictedList[0])) # A
            predicted += str(int(predictedList[1])) # B
            predicted += str(int(predictedList[2])) # C
            predicted += str(int(predictedList[3])) # D
            predicted += str(int(predictedList[4])) # E
            predicted += str(int(predictedList[5])) # F
            predicted += str(int(predictedList[6])) # G

            probablity = 0.0
            if (hasProbas):
                lableAIndex = labelEncoderA.transform(predictedList[0])
                lableBIndex = labelEncoderB.transform(predictedList[1])
                lableCIndex = labelEncoderC.transform(predictedList[2])
                lableDIndex = labelEncoderD.transform(predictedList[3])
                lableEIndex = labelEncoderE.transform(predictedList[4])
                lableFIndex = labelEncoderF.transform(predictedList[5])
                lableGIndex = labelEncoderG.transform(predictedList[6])

                probablityLogA = probasLogAllMatrix[0][rowIndex][lableAIndex]
                probablityLogB = probasLogAllMatrix[1][rowIndex][lableBIndex]
                probablityLogC = probasLogAllMatrix[2][rowIndex][lableCIndex]
                probablityLogD = probasLogAllMatrix[3][rowIndex][lableDIndex]
                probablityLogE = probasLogAllMatrix[4][rowIndex][lableEIndex]
                probablityLogF = probasLogAllMatrix[5][rowIndex][lableFIndex]
                probablityLogG = probasLogAllMatrix[6][rowIndex][lableGIndex]

                #probablityA = probasAllMatrix[0][rowIndex][lableAIndex] # For debugging only
                #probablityB = probasAllMatrix[1][rowIndex][lableBIndex]
                #probablityC = probasAllMatrix[2][rowIndex][lableCIndex]
                #probablityD = probasAllMatrix[3][rowIndex][lableDIndex]
                #probablityE = probasAllMatrix[4][rowIndex][lableEIndex]
                #probablityF = probasAllMatrix[5][rowIndex][lableFIndex]
                #probablityG = probasAllMatrix[6][rowIndex][lableGIndex]

                #probablityOld = probablityA * probablityB * probablityC * probablityD * probablityE * probablityF * probablityG # For debugging only
                probablityLog = probablityLogA + probablityLogB + probablityLogC + probablityLogD + probablityLogE + probablityLogF + probablityLogG
                probablity = math.exp(probablityLog)


            row = [dataID, predicted, probablity]
            rows.append(row)

        paramDict = {}
        paramDict['modelName'] = modelName
        paramDict['model'] = model
        self.Loop_INSERT(rows, rowHeader, self.__DRV_PredictRow, paramDict)
        print ''

    # Get Feature Dataform (dfX), Results Series (dfY) and DataID Series (dfDataID)
    # featuresColumns = Example: "Pclass, A_TitleHash"
    # dataType = "Train"=(1), "Cross"=(2), "Test"=(3) or ALL=(*)
    # PreProcessDataFrame = Function used to modify and pre-process columns. Signature df=PreProcessDataFrame(df)
    # WARNING: You must get all DataType and filter DataFrame else you will not have the identical columns after OneHotDataframe
    # Called from ModelXxxxx
    def GetFeaturesAndResults(self, featuresColumns, dataType, preProcessDataFrame=None, viewName='[dbo].[WRK_Train_vw]'):
        selectSql = "SELECT DataID, P_A,P_B,P_C,P_D,P_E,P_F,P_G, " + featuresColumns + ", DataType" + " FROM " + viewName + " ORDER BY [DataID]"

        df = self.GetRowsDataFrameFromSelect(selectSql)
        if (preProcessDataFrame is not None):
            df = preProcessDataFrame(df) # Column manipulation for model

        # Filter required DataType
        if (dataType == "Train"):
            df = df[(df.DataType == 1) | (df.DataType == 9)]
        elif (dataType == "Cross"):
            df = df[(df.DataType == 2)]
        elif (dataType == "Test"):
            df = df[(df.DataType == 3)]

        df = df.drop(['DataType'], axis=1)

        dfDataID = df[['DataID']]
        dfY = df[['P_A', 'P_B', 'P_C', 'P_D', 'P_E', 'P_F', 'P_G']].astype(np.float)
        dfY.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        dfX = df.drop(['DataID', 'P_A', 'P_B', 'P_C', 'P_D', 'P_E', 'P_F', 'P_G'], axis=1).astype(np.float) 
        df = None
        print '  ' + dataType + '_X = ' + str(dfX.shape)
        print '  ' + dataType + '_Y = ' + str(dfY.shape)
        print '  ' + dataType + '_DataID = ' + str(dfDataID.shape)

        return (dfX, dfY, dfDataID) 

    # Get Feature Dataform (dfX), Results Series (dfY) and DataID Series (dfDataID) from DATA_Cache otherwise SQL
    # If cache exists there is no need to access SQL
    # featuresColumns = Example: "Pclass, A_TitleHash"
    # dataType = "Train"=(1), "Cross"=(2), "Test"=(3) or ALL=(*)
    # modelName = "Base"
    # PreProcessDataFrame = Function used to modify and pre-process columns. Signature df=PreProcessDataFrame(df)
    # WARNING: You must get all DataType and filter DataFrame else you will not have the identical columns after OneHotDataframe
    # Called from ModelXxxxx
    def GetFeaturesAndResultsFromCache(self, featuresColumns, dataType, modelName, preProcessDataFrame, viewName='[dbo].[WRK_Train_vw]'):
        dfY = self.__GetDataFrameFromCache(dataType, modelName, 'Y') # Assume if Y exists, then the other matrix also exist
        if (dfY is None):
            dfX, dfY, dfDataID = self.GetFeaturesAndResults(featuresColumns=featuresColumns, dataType=dataType, preProcessDataFrame=preProcessDataFrame, viewName=viewName)
            self. __CacheDataFrame(dfX, dataType, modelName, 'X')
            self. __CacheDataFrame(dfY, dataType, modelName, 'Y')
            self. __CacheDataFrame(dfDataID, dataType, modelName, 'DataID')
        else:
            dfX = self.__GetDataFrameFromCache(dataType, modelName, 'X')
            dfDataID = self.__GetDataFrameFromCache(dataType, modelName, 'DataID')

        print '  ' + dataType + '_X = ' + str(dfX.shape)
        print '  ' + dataType + '_Y = ' + str(dfY.shape)
        print '  ' + dataType + '_DataID = ' + str(dfDataID.shape)

        return (dfX, dfY, dfDataID)

    def __GetDataFrameFromCache(self, dataType, modelName, matrixType):
        fileUNC = self.CacheFolderUNC + dataType + '_' + matrixType + '_' + modelName + '.tab'
        if (os.path.isfile(fileUNC)):
            print '  Read from cache: ' + fileUNC
            df = pd.read_csv(fileUNC, sep='\t')
        else:
            df = None

        return df

    def __CacheDataFrame(self, df, dataType, modelName, matrixType):
        fileUNC = self.CacheFolderUNC + dataType + '_' + matrixType + '_' + modelName + '.tab'
        print '  Write to cache: ' + fileUNC
        df.to_csv(fileUNC, sep='\t', index=False)

