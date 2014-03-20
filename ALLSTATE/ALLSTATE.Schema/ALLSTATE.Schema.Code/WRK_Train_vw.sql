IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.WRK_Train_vw') AND OBJECTPROPERTY(id, 'IsView') = 1))
    DROP VIEW dbo.WRK_Train_vw
GO

/**************************************************
File: WRK_Train_vw.sql

Description: Used for training alorithm

History:
2014-01-03    Create  Created
**************************************************/
CREATE VIEW [dbo].[WRK_Train_vw] AS

SELECT
 [RAW_Data].[DataID]
,[RAW_Data].[DataType]
,CAST([RAW_Data].[Actual] AS FLOAT) AS [Actual]
,[RAW_Data].[Pclass]
,[WRK_Data].[SexINT]
,[WRK_Data].[SalutationHash]
,[WRK_Data].[EmbarkedINT]
,[WRK_Data].[AgeFLOAT]
,[WRK_Data].[FareFLOAT]
,dbo.SafeLOG10_fn([WRK_Data].[FareFLOAT]) AS [FareLOG10]
,CAST([WRK_Data].[IsChild] AS FLOAT) AS [IsChild]
,CAST([WRK_Data].[IsAdult] AS FLOAT) AS [IsAdult]
,CAST([WRK_Data].[HasFamily] AS FLOAT) AS [HasFamily]
,CAST([WRK_Data].[HasParent] AS FLOAT) AS [HasParent]
,CAST([WRK_Data].[HasChild] AS FLOAT) AS [HasChild]
,CAST([WRK_Data].[HasSpouse] AS FLOAT) AS [HasSpouse]
,CAST([WRK_Data].[HasSibling] AS FLOAT) AS [HasSibling]
,[WRK_Data].[Parents]
,[WRK_Data].[Children]
,[WRK_Data].[Sibling]
,[WRK_Data].[DeptCodeHash]
,[WRK_Data].[DeckHash]
,[WRK_Data].[A_TitleHash]
,[WRK_Data].[DualOccupant]
,[WRK_Data].[OtherSurvivers]
,[WRK_Data].[HasOtherSurviver]
,[WRK_Data].[OtherDied]
,[WRK_Data].[HasOtherDied]
FROM [dbo].[RAW_Data]
JOIN [dbo].[WRK_Data]
  ON [WRK_Data].[DataID] = [RAW_Data].[DataID]
--WHERE [RAW_Data].[DataType] IN (1, 2, 3, 9) -- Selection done in .py

GO

GRANT SELECT, VIEW DEFINITION ON dbo.WRK_Train_vw TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT * FROM [dbo].[WRK_Train_vw] WHERE [DataType] IN (3)
SELECT * FROM [dbo].[WRK_Train_vw] WHERE [DeptCodeHash]=93
*****************************************************/
