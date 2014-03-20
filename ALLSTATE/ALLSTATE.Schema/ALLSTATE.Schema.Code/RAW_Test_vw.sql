IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.RAW_Test_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo. RAW_Test_vw
GO

/**************************************************
File: RAW_Test_vw.sql

Description: RAW_Data view of Test data
    
History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW dbo.RAW_Test_vw AS
SELECT
 [DataID]
,[DataType] -- 3
,[PassengerId]
,[Pclass]
,[Name]
,[Sex]
,[Age]
,[SibSp]
,[ParCh]
,[Ticket]
,[Fare]
,[Cabin]
,[Embarked]
FROM [dbo].[RAW_Data]
WHERE [DataType] = 3 -- Test

GO

GRANT SELECT, VIEW DEFINITION ON dbo.RAW_Test_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM dbo.RAW_Test_vw
*****************************************************/
