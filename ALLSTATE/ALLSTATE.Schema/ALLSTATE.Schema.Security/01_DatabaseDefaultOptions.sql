/**************************************************
File: 01_DatabaseDefaultOptions.sql

Description: Set Database default options.
         This is the only way to set options like ARITHABORT
         so that DTS Packages run.
         Ref: http://www.codecomments.com/archive352-2005-3-440293.html


    The ARITHABORT ON connection option is required in order to modify a table
    with indexed views or indexes on computed columns.
    EMP_Employee has an Indexed View.

History:
2014-01-02 Trevor      Created.
**************************************************/
PRINT 'SET DATABASE DEAFULT OPTIONS'
ALTER DATABASE <MSX:TITANIC.ConnectionString.Database>
    SET ARITHABORT ON
GO

PRINT 'SET DATABASE BACKUP TYPE TO - FULL (TRANSACTION LOGGING)'
ALTER DATABASE <MSX:TITANIC.ConnectionString.Database> SET RECOVERY FULL
GO
PRINT 'EXTENDED DATABASE PROPERTIES'
EXEC dbo.UTL_DatabaseExtenedProperty_sp 'Database Description', 'KAGGLE TITANIC Competition.'
EXEC dbo.UTL_DatabaseExtenedProperty_sp 'ITS Contact', 'Trevor@deloitte.com.au'
EXEC dbo.UTL_DatabaseExtenedProperty_sp 'Reserved by', 'Trevor@deloitte.com.au'
EXEC dbo.UTL_DatabaseExtenedProperty_sp 'Reserved till', '1900-01-01'
EXEC dbo.UTL_DatabaseExtenedProperty_sp 'Remove after', '9999-12-31'

SELECT name, value FROM  ::FN_LISTEXTENDEDPROPERTY(NULL,NULL,NULL,NULL,NULL,NULL,NULL)
GO
