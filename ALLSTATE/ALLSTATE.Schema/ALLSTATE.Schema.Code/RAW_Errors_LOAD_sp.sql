IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.RAW_Errors_LOAD_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.RAW_Errors_LOAD_sp
GO

/**************************************************
File: RAW_Errors_LOAD_sp.sql

Description: Predicted errors that are extracted to be added to Train.csv to boost results.

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.RAW_Errors_LOAD_sp
 @Interation INT = 1
AS
SET NOCOUNT ON -- Required for VBA

DECLARE @Offset_PassengerId INT
SET @Offset_PassengerId = @Interation * 1500

SELECT 
 PassengerId + @Offset_PassengerId AS PassengerId
,Actual AS Survived
,Pclass
,Name
,Sex
,Age
,SibSp
,ParCh
,Ticket
,Fare
,Cabin
,Embarked
FROM dbo.RAW_Data
JOIN dbo.RAW_Errors_vw
  ON RAW_Errors_vw.DataID = RAW_Data.DataID
ORDER BY RAW_Errors_vw.DataID
 
GO

GRANT EXEC, VIEW DEFINITION ON dbo.RAW_Errors_LOAD_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.RAW_Errors_LOAD_sp @Interation=2
*****************************************************/
