#!/usr/bin/python
import pymssql
import SharedLibrary
from ConnectionSQL import ConnectionSQL
import Context

def Execute(context):
    connectionSQL = ConnectionSQL(context)

    connectionSQL.TruncateTable("[dbo].[WRK_Data]")

    #rowHeader = "INSERT [dbo].[WRK_Data] (DataID,[SexINT]) VALUES\n"
    rowHeader = "INSERT [dbo].[WRK_Data] (DataID) VALUES\n"
    rows = connectionSQL.GetRowsDictFromSelect("SELECT * FROM [dbo].[RAW_Data] ORDER BY [DataID]")
    connectionSQL.Loop_INSERT(rows, rowHeader, FunctProcessRow)
    connectionSQL.Execute("EXEC dbo.WRK_Data_UPDATE_CrossRow_sp")

# Generate SQL to insert a single row, without "(" and ")"
def FunctProcessRow(row, paramDict):
    sql = ""

    DataID = row['DataID']
    #Sex = row['Sex']

    #SexINT = SharedLibrary.SexINT(Sex)

    sql +=  str(DataID)
    #sql += "," + str(SexINT)

    return sql

