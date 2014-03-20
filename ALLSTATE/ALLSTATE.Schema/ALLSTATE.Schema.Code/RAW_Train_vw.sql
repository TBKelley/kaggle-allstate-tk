IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.RAW_Train_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.RAW_Train_vw
GO

/**************************************************
File: RAW_Train_vw.sql

Description: RAW_Data view of Training data
    
History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW dbo.RAW_Train_vw AS
SELECT
 DataID
,[Actual] AS [Survived]
,PassengerId
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
FROM [dbo].[RAW_Data]
WHERE [DataType] IN  (1, 9) -- Train, Boost

GO

GRANT SELECT, VIEW DEFINITION ON dbo.RAW_Train_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM dbo.RAW_Train_vw
*****************************************************/
