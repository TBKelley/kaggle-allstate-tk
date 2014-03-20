IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo. WRK_Data_CSV_LOAD_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo. WRK_Data_CSV_LOAD_sp
GO

/**************************************************
File: WRK_Data_CSV_LOAD_sp.sql

Description: Used to generate train.csv, test.csv

History:
2014-01-05    Create  Created
**************************************************/
CREATE PROCEDURE dbo. WRK_Data_CSV_LOAD_sp
AS
SET NOCOUNT ON -- Required for VBA

SELECT
 [RAW_Data].[DataID]
,[RAW_Data].[Actual] AS [Survived]
,[RAW_Data].[PassengerId]
,[RAW_Data].[Pclass]
,[RAW_Data].[Name]
,[RAW_Data].[Sex]
,[RAW_Data].[Age]
,[RAW_Data].[SibSp]
,[RAW_Data].[ParCh]
,[RAW_Data].[Ticket]
,[RAW_Data].[Fare]
,[RAW_Data].[Cabin]
,[RAW_Data].[Embarked]
,[WRK_Data].[SexINT]
,[WRK_Data].[Salutation]
,[WRK_Data].[SalutationHash]
,[WRK_Data].[EmbarkedINT]
,[WRK_Data].[AgeFLOAT]
,[WRK_Data].[FareFLOAT]
,[WRK_Data].[IsChild]
,[WRK_Data].[IsAdult]
,[WRK_Data].[HasFamily]
,[WRK_Data].[HasParent]
,[WRK_Data].[HasChild]
,[WRK_Data].[HasSpouse]
,[WRK_Data].[HasSibling]
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
WHERE [DataType] = 1 -- Train
ORDER BY [RAW_Data].[DataID]

SELECT
 [RAW_Data].[DataID]
,[RAW_Data].[Actual] AS [Survived]
,[RAW_Data].[PassengerId]
,[RAW_Data].[Pclass]
,[RAW_Data].[Name]
,[RAW_Data].[Sex]
,[RAW_Data].[Age]
,[RAW_Data].[SibSp]
,[RAW_Data].[ParCh]
,[RAW_Data].[Ticket]
,[RAW_Data].[Fare]
,[RAW_Data].[Cabin]
,[RAW_Data].[Embarked]
,[WRK_Data].[SexINT]
,[WRK_Data].[Salutation]
,[WRK_Data].[SalutationHash]
,[WRK_Data].[EmbarkedINT]
,[WRK_Data].[AgeFLOAT]
,[WRK_Data].[FareFLOAT]
,[WRK_Data].[IsChild]
,[WRK_Data].[IsAdult]
,[WRK_Data].[HasFamily]
,[WRK_Data].[HasParent]
,[WRK_Data].[HasChild]
,[WRK_Data].[HasSpouse]
,[WRK_Data].[HasSibling]
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
WHERE [DataType] = 2 -- Test
ORDER BY [RAW_Data].[DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo. WRK_Data_CSV_LOAD_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo. WRK_Data_CSV_LOAD_sp
*****************************************************/

