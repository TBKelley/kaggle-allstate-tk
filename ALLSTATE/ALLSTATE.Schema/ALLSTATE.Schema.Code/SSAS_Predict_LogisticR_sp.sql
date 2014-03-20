IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.SSAS_Predict_LogisticR_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.SSAS_Predict_LogisticR_sp
GO

/**************************************************
File: SSAS_Predict_LogisticR_sp.sql

Description: Create predictive table SSAS_Predict_LogisticR

RMSE=0.61+/-0.01 10%:>1.64%

History:
2013-11-01    TrKelley  Created
**************************************************/
CREATE PROCEDURE dbo.SSAS_Predict_LogisticR_sp
AS
DECLARE @Model VARCHAR(50)
SET @Model = 'LogisticR'

SET NOCOUNT ON

IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.SSAS_Predict_LogisticR') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.[SSAS_Predict_LogisticR]

SELECT *
INTO [dbo].[SSAS_Predict_LogisticR]
FROM OPENQUERY([SSAS], 
'SELECT
  t.[DataID],
  (Predict([LogisticR].[Actual])) as [Predicted],
  (PredictProbability([LogisticR].[Actual],1)) as [Probablity],
  (PredictAdjustedProbability([LogisticR].[Actual],1)) as [ProbablityAdj]
From
  [LogisticR]
PREDICTION JOIN
  OPENQUERY([TITANIC],
    ''SELECT
      [DataID],
      [Actual],
      [Pclass],
      [SexINT],
      [SalutationHash],
      [EmbarkedINT],
      [AgeFLOAT],
      [FareFLOAT],
      [IsChild],
      [IsAdult],
      [HasFamily],
      [HasParent],
      [HasChild],
      [HasSpouse],
      [HasSibling],
      [Parents],
      [Children],
      [Sibling],
      [DeptCodeHash],
      [DeckHash]
    FROM
      [dbo].[DRV_Full_SSAS_vw]
    '') AS t
ON
  [LogisticR].[Actual] = t.[Actual] AND
  [LogisticR].[Pclass] = t.[Pclass] AND
  [LogisticR].[Sex INT] = t.[SexINT] AND
  [LogisticR].[Salutation Hash] = t.[SalutationHash] AND
  [LogisticR].[Embarked INT] = t.[EmbarkedINT] AND
  [LogisticR].[Age FLOAT] = t.[AgeFLOAT] AND
  [LogisticR].[Fare FLOAT] = t.[FareFLOAT] AND
  [LogisticR].[Is Child] = t.[IsChild] AND
  [LogisticR].[Is Adult] = t.[IsAdult] AND
  [LogisticR].[Has Family] = t.[HasFamily] AND
  [LogisticR].[Has Parent] = t.[HasParent] AND
  [LogisticR].[Has Child] = t.[HasChild] AND
  [LogisticR].[Has Spouse] = t.[HasSpouse] AND
  [LogisticR].[Has Sibling] = t.[HasSibling] AND
  [LogisticR].[Parents] = t.[Parents] AND
  [LogisticR].[Children] = t.[Children] AND
  [LogisticR].[Sibling] = t.[Sibling] AND
  [LogisticR].[Dept Code Hash] = t.[DeptCodeHash] AND
  [LogisticR].[Deck Hash] = t.[DeckHash]
') Model
ORDER BY Model.[DataID]

DELETE [dbo].[DRV_Predict] WHERE [Model] = @Model

INSERT [dbo].[DRV_Predict] ([Model], [DataID], [Predicted], [Probablity])
SELECT
 @Model AS [Model]
,[DataID]
,[Predicted]
,[Probablity]
FROM [dbo].[SSAS_Predict_LogisticR]
ORDER BY [DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.SSAS_Predict_LogisticR_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.SSAS_Predict_LogisticR_sp
SELECT TOP 10 * FROM [dbo].[SSAS_Predict_LogisticR] ORDER BY [DataID]
SELECT TOP 10 * FROM [dbo].[DRV_Predict] WHERE [Model]='LogisticR'
*****************************************************/

