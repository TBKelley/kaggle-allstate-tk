import csv as csv
import numpy as np
import pymssql
import pandas.io.sql as sql
import SharedLibrary
import Context

class ConnectionSQL(object):
    """
    Connection class used to encapulate SQL methods.
    """
    def __init__(self, context): 
        self.__mssqlInstance = context.MssqlInstance
        self.__mssqlDatabase = context.MssqlDatabase
        self.__mssqlUser = context.MssqlUser
        self.__mssqlPassword = context.MssqlPassword
        self.__batch_size = 1000 # MSSQL Max is 1,000

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

    # TRUNCATE MSSQL TableName, resetting any INT IDENTITY(Start,Increment)
    def TruncateTable(self, TableName):
        self.Execute("TRUNCATE TABLE " + TableName)

    # Execute SelectSql and retuen a list of row tuplets
    # Returns a list of row tuplets [(10, 3, 80, 0, 1.0), (11, 2, 82, 1, 2.0), ...]
    def GetRowsListFromSelect(self, SelectSql):      
        conn = self.Connect()
        cur = self.Cursor(conn)

        print SelectSql
        cur.execute(SelectSql)
        print 'FetchAll rows'
        rows = cur.fetchall() # Must cache all to avoid connection closing issues in execute(sql)
        print '  Rows cached = ' + str(len(rows))
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
        print '  Rows cached = ' + str(len(rows))
        conn.close()
        return rows

    # Execute SelectSql and return pandas DataFrame of rows.
    # Returns pandas DataFrame of SQL rows 
    def GetRowsDataFrameFromSelect(self, SelectSql):
        conn = self.Connect(as_dict=False)    
        print SelectSql
        df = sql.read_frame(SelectSql, conn)
        
        print '  Rows cached = ' + str(df.shape[0])
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
        print 'DONE... ' + str(row_counter) + ' rows inserted into [' + self.MssqlInstance + '].[' + self.MssqlDatabase + '].' + mssqlTable
        print ''

    # INSERT rows to an MSSQL table defined by RowHeader and rows formatted by FunctProcessRow
    # rows = List of lists [[Col1Value, Col2Value, ...] [Col1Value, Col2Value, ...]]
    # RowHeader = INSERT SQL. Example: "INSERT [dbo].[DRV_Predict] (Model, DataID, Predicted, Probablity) VALUES\n"
    # FunctProcessRow = Function used to format a single row without brackets. Example: "'Col1Value', Col2Value, 'Col3Value'"
    # paramDict = NOT USED!  Parameter dictionary {'modelName':'Base', 'model':clfModel}
    def Loop_INSERT(self, rows, RowHeader, FunctProcessRow, paramDict=None):
        conn = self.Connect()
        cur = self.Cursor(conn)

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
        print 'DONE... ' + str(row_counter) + ' rows inserted.'
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
        sql += "," + str(Predicted)
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
    
        predictAllList = model.predict(all_X)

        hasProbas = False
        try:
            probasAllMatrix = model.predict_proba(all_X)
            hasProbas = True
        except AttributeError:
            pass ## Ignore

        rows = []
        for index in range(len(predictAllList)):
            DataID = all_DataID[index]
            Predicted = int(predictAllList[index])
            Probablity = 0.0
            if (hasProbas):
                Probablity = probasAllMatrix[index][1]
            row = [DataID, Predicted, Probablity]
            rows.append(row)

        paramDict = {}
        paramDict['modelName'] = modelName
        paramDict['model'] = model
        self.Loop_INSERT(rows, rowHeader, self.__DRV_PredictRow, paramDict)
        print ''

    # Get Feature Dataform (dfX), Results Series (dfY) and DataID Series (dfDataID)
    # featuresColumns = Example: "Pclass, A_TitleHash"
    # dataType = "Train"=(1,9), "Cross"=(2), "Test"=(3) or ALL=(*)
    # PreProcessDataFrame = Function used to modify and pre-process columns. Signature df=PreProcessDataFrame(df)
    # WARNING: You must get all DataType and filter DataFrame else you will not have the identical columns after OneHotDataframe
    # Called from ModelXxxxx
    def GetFeaturesAndResults(self, featuresColumns, dataType, PreProcessDataFrame):
        selectSql = "SELECT DataID, Actual, " + featuresColumns + ", DataType" + " FROM [dbo].[WRK_Train_vw] ORDER BY [WRK_Train_vw].[DataID]"

        df = self.GetRowsDataFrameFromSelect(selectSql)
        df = PreProcessDataFrame(df) # Column manipulation for model

        # Filter required DataType
        if (dataType == "Train"):
            df = df[(df.DataType == 1) | (df.DataType == 9)]
        elif (dataType == "Cross"):
            df = df[(df.DataType == 2)]
        elif (dataType == "Test"):
            df = df[(df.DataType == 3)]

        df = df.drop(['DataType'], axis=1)

        dfDataID = df['DataID']
        dfY = df['Actual'].astype(np.float)
        dfX = df.drop(['DataID', 'Actual'], axis=1).astype(np.float) 
        df = None
        print '  ' + dataType + '_X = ' + str(dfX.shape)
        print '  ' + dataType + '_Y = ' + str(dfY.shape)
        print '  ' + dataType + '_DataID = ' + str(dfDataID.shape)

        return (dfX, dfY, dfDataID) 