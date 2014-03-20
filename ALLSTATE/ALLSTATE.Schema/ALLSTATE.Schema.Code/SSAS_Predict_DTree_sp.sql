IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.SSAS_Predict_DTree_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.SSAS_Predict_DTree_sp
GO

/**************************************************
File: SSAS_Predict_DTree_sp.sql

Description: Create predictive table SSAS_Predict_DTree

RMSE=0.61+/-0.01 10%:>1.64%

History:
2013-11-01    TrKelley  Created
**************************************************/
CREATE PROCEDURE dbo.SSAS_Predict_DTree_sp
AS
DECLARE @Model VARCHAR(50)
SET @Model = 'DTree'

SET NOCOUNT ON

IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.SSAS_Predict_DTree') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.[SSAS_Predict_DTree]

SELECT *
INTO [dbo].[SSAS_Predict_DTree]
FROM OPENQUERY([SSAS], 
'SELECT
  t.[DataID],
  (Predict([DTree].[Actual])) as [Predicted],
  (PredictProbability([DTree].[Actual],1)) as [Probablity],
  (PredictAdjustedProbability([DTree].[Actual],1)) as [ProbablityAdj]
From
  [DTree]
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
  [DTree].[Actual] = t.[Actual] AND
  [DTree].[Pclass] = t.[Pclass] AND
  [DTree].[Sex INT] = t.[SexINT] AND
  [DTree].[Salutation Hash] = t.[SalutationHash] AND
  [DTree].[Embarked INT] = t.[EmbarkedINT] AND
  [DTree].[Age FLOAT] = t.[AgeFLOAT] AND
  [DTree].[Fare FLOAT] = t.[FareFLOAT] AND
  [DTree].[Is Child] = t.[IsChild] AND
  [DTree].[Is Adult] = t.[IsAdult] AND
  [DTree].[Has Family] = t.[HasFamily] AND
  [DTree].[Has Parent] = t.[HasParent] AND
  [DTree].[Has Child] = t.[HasChild] AND
  [DTree].[Has Spouse] = t.[HasSpouse] AND
  [DTree].[Has Sibling] = t.[HasSibling] AND
  [DTree].[Parents] = t.[Parents] AND
  [DTree].[Children] = t.[Children] AND
  [DTree].[Sibling] = t.[Sibling] AND
  [DTree].[Dept Code Hash] = t.[DeptCodeHash] AND
  [DTree].[Deck Hash] = t.[DeckHash]
') Model
ORDER BY Model.[DataID]

DELETE [dbo].[DRV_Predict] WHERE [Model] = @Model

INSERT [dbo].[DRV_Predict] ([Model], [DataID], [Predicted], [Probablity])
SELECT
 @Model AS [Model]
,[DataID]
,[Predicted]
,[Probablity]
FROM [dbo].[SSAS_Predict_DTree]
ORDER BY [DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.SSAS_Predict_DTree_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.SSAS_Predict_DTree_sp
SELECT TOP 10 * FROM [dbo].[SSAS_Predict_DTree] ORDER BY [DataID]
SELECT TOP 10 * FROM [dbo].[DRV_Predict] WHERE [Model]='DTree'
*****************************************************/

