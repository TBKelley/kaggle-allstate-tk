IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.SSAS_Predict_NNetwork_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.SSAS_Predict_NNetwork_sp
GO

/**************************************************
File: SSAS_Predict_NNetwork_sp.sql

Description: Create predictive table SSAS_Predict_NNetwork

RMSE=0.61+/-0.01 10%:>1.64%

History:
2013-11-01    TrKelley  Created
**************************************************/
CREATE PROCEDURE dbo.SSAS_Predict_NNetwork_sp
AS
DECLARE @Model VARCHAR(50)
SET @Model = 'NNetwork'

SET NOCOUNT ON

IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.SSAS_Predict_NNetwork') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.[SSAS_Predict_NNetwork]

SELECT *
INTO [dbo].[SSAS_Predict_NNetwork]
FROM OPENQUERY([SSAS], 
'SELECT
  t.[DataID],
  (Predict([NNetwork].[Actual])) as [Predicted],
  (PredictProbability([NNetwork].[Actual],1)) as [Probablity],
  (PredictAdjustedProbability([NNetwork].[Actual],1)) as [ProbablityAdj]
From
  [NNetwork]
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
  [NNetwork].[Actual] = t.[Actual] AND
  [NNetwork].[Pclass] = t.[Pclass] AND
  [NNetwork].[Sex INT] = t.[SexINT] AND
  [NNetwork].[Salutation Hash] = t.[SalutationHash] AND
  [NNetwork].[Embarked INT] = t.[EmbarkedINT] AND
  [NNetwork].[Age FLOAT] = t.[AgeFLOAT] AND
  [NNetwork].[Fare FLOAT] = t.[FareFLOAT] AND
  [NNetwork].[Is Child] = t.[IsChild] AND
  [NNetwork].[Is Adult] = t.[IsAdult] AND
  [NNetwork].[Has Family] = t.[HasFamily] AND
  [NNetwork].[Has Parent] = t.[HasParent] AND
  [NNetwork].[Has Child] = t.[HasChild] AND
  [NNetwork].[Has Spouse] = t.[HasSpouse] AND
  [NNetwork].[Has Sibling] = t.[HasSibling] AND
  [NNetwork].[Parents] = t.[Parents] AND
  [NNetwork].[Children] = t.[Children] AND
  [NNetwork].[Sibling] = t.[Sibling] AND
  [NNetwork].[Dept Code Hash] = t.[DeptCodeHash] AND
  [NNetwork].[Deck Hash] = t.[DeckHash]
') Model
ORDER BY Model.[DataID]

DELETE [dbo].[DRV_Predict] WHERE [Model] = @Model

INSERT [dbo].[DRV_Predict] ([Model], [DataID], [Predicted], [Probablity])
SELECT
 @Model AS [Model]
,[DataID]
,[Predicted]
,[Probablity]
FROM [dbo].[SSAS_Predict_NNetwork]
ORDER BY [DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.SSAS_Predict_NNetwork_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.SSAS_Predict_NNetwork_sp
SELECT TOP 10 * FROM [dbo].[SSAS_Predict_NNetwork] ORDER BY [DataID]
SELECT TOP 10 * FROM [dbo].[DRV_Predict] WHERE [Model]='NNetwork'
*****************************************************/

