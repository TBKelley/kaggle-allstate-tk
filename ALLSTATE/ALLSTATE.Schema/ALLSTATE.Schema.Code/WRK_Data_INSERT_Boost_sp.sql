IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.WRK_Data_INSERT_Boost_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.WRK_Data_INSERT_Boost_sp
GO

/**************************************************
File: WRK_Data_INSERT_Boost_sp.sql

Description: INSERT Failed rows into RAW_Data, WRK_Data.

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.WRK_Data_INSERT_Boost_sp
AS
SET NOCOUNT ON -- Required for VBA

INSERT dbo.[RAW_Data] (DataType, Actual, PassengerId, Pclass, Name, Sex, Age, SibSp, ParCh, Ticket, Fare, Cabin, Embarked)
SELECT 
 128 AS [DataType] -- Tempary marker
,[RAW_Data].Actual
,[RAW_Data].PassengerId
,[RAW_Data].Pclass
,[RAW_Data].Name
,[RAW_Data].Sex
,[RAW_Data].Age
,[RAW_Data].SibSp
,[RAW_Data].ParCh
,[RAW_Data].Ticket
,[RAW_Data].Fare
,[RAW_Data].Cabin
,[RAW_Data].Embarked
FROM [dbo].[RAW_Data]
JOIN [dbo].[RAW_Data_FAILED_vw]
  ON [RAW_Data_FAILED_vw].[DataID] = [RAW_Data].[DataID]
ORDER BY [RAW_Data_FAILED_vw].[DataID]

INSERT [dbo].[WRK_Data] (DataID, SexINT, Salutation, SalutationHash, EmbarkedINT, AgeFLOAT, FareFLOAT, IsChild, IsAdult, HasFamily, HasParent, HasChild, HasSpouse, HasSibling, Parents, Children, Sibling, DeptCodeHash, DeckHash, A_TitleHash, DualOccupant, OtherSurvivers, HasOtherSurviver, OtherDied, HasOtherDied)
SELECT
 [NEW_RAW_Data].DataID
,[WRK_Data].SexINT
,[WRK_Data].Salutation
,[WRK_Data].SalutationHash
,[WRK_Data].EmbarkedINT
,[WRK_Data].AgeFLOAT
,[WRK_Data].FareFLOAT
,[WRK_Data].IsChild
,[WRK_Data].IsAdult
,[WRK_Data].HasFamily
,[WRK_Data].HasParent
,[WRK_Data].HasChild
,[WRK_Data]. HasSpouse
,[WRK_Data].HasSibling
,[WRK_Data].Parents
,[WRK_Data].Children
,[WRK_Data].Sibling
,[WRK_Data].DeptCodeHash
,[WRK_Data].DeckHash
,[WRK_Data].A_TitleHash
,[WRK_Data].DualOccupant
,[WRK_Data].OtherSurvivers
,[WRK_Data].HasOtherSurviver
,[WRK_Data].OtherDied
,[WRK_Data].HasOtherDied
FROM [dbo].[WRK_Data]
JOIN [dbo].[RAW_Data_FAILED_vw]
  ON [RAW_Data_FAILED_vw].[DataID] = [WRK_Data].[DataID]
JOIN [dbo].[RAW_Data] [OLD_RAW_Data]
  ON [OLD_RAW_Data].[DataID] = [WRK_Data].[DataID]
JOIN [dbo].[RAW_Data] [NEW_RAW_Data]
  ON [NEW_RAW_Data].[PassengerId] = [OLD_RAW_Data].[PassengerId]
 AND [NEW_RAW_Data].[DataType] = 128
ORDER BY [NEW_RAW_Data].[PassengerId]

UPDATE dbo.[RAW_Data] SET
[DataType] = 9
WHERE [DataType] = 128

GO

GRANT EXEC, VIEW DEFINITION ON dbo.WRK_Data_INSERT_Boost_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT COUNT(*) AS [RAW_Data Records] FROM [dbo].[RAW_Data]
SELECT COUNT(*) AS [WRK_Data Records] FROM [dbo].[WRK_Data]
EXEC dbo.WRK_Data_INSERT_Boost_sp
SELECT COUNT(*) AS [RAW_Data Records] FROM [dbo].[RAW_Data]
SELECT COUNT(*) AS [WRK_Data Records] FROM [dbo].[WRK_Data]
*****************************************************/
