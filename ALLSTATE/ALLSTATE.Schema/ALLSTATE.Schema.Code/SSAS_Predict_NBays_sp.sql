IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.SSAS_Predict_NBays_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.SSAS_Predict_NBays_sp
GO

/**************************************************
File: SSAS_Predict_NBays_sp.sql

Description: Create predictive table SSAS_Predict_NBays

RMSE=0.61+/-0.01 10%:>1.64%

History:
2013-11-01    TrKelley  Created
**************************************************/
CREATE PROCEDURE dbo.SSAS_Predict_NBays_sp
AS
DECLARE @Model VARCHAR(50)
SET @Model = 'NBays'

SET NOCOUNT ON

IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.SSAS_Predict_NBays') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.[SSAS_Predict_NBays]

SELECT *
INTO [dbo].[SSAS_Predict_NBays]
FROM OPENQUERY([SSAS], 
'SELECT
  t.[DataID],
  (Predict([NBays].[Actual])) as [Predicted],
  (PredictProbability([NBays].[Actual],1)) as [Probablity],
  (PredictAdjustedProbability([NBays].[Actual],1)) as [ProbablityAdj]
From
  [NBays]
PREDICTION JOIN
  OPENQUERY([TITANIC],
    ''SELECT
      [DataID],
      [Actual],
      [Pclass],
      [SexINT],
      [SalutationHash],
      [EmbarkedINT],
      [IsChild],
      [IsAdult],
      [HasFamily],
      [HasParent],
      [HasChild],
      [HasSpouse],
      [HasSibling],
      [DeptCodeHash],
      [DeckHash]
    FROM
      [dbo].[DRV_Full_SSAS_vw]
    '') AS t
ON
  [NBays].[Actual] = t.[Actual] AND
  [NBays].[Pclass] = t.[Pclass] AND
  [NBays].[Sex INT] = t.[SexINT] AND
  [NBays].[Salutation Hash] = t.[SalutationHash] AND
  [NBays].[Embarked INT] = t.[EmbarkedINT] AND
  [NBays].[Is Child] = t.[IsChild] AND
  [NBays].[Is Adult] = t.[IsAdult] AND
  [NBays].[Has Family] = t.[HasFamily] AND
  [NBays].[Has Parent] = t.[HasParent] AND
  [NBays].[Has Child] = t.[HasChild] AND
  [NBays].[Has Spouse] = t.[HasSpouse] AND
  [NBays].[Has Sibling] = t.[HasSibling] AND
  [NBays].[Dept Code Hash] = t.[DeptCodeHash] AND
  [NBays].[Deck Hash] = t.[DeckHash]
') Model
ORDER BY Model.[DataID]

DELETE [dbo].[DRV_Predict] WHERE [Model] = @Model

INSERT [dbo].[DRV_Predict] ([Model], [DataID], [Predicted], [Probablity])
SELECT
 @Model AS [Model]
,[DataID]
,[Predicted]
,[Probablity]
FROM [dbo].[SSAS_Predict_NBays]
ORDER BY [DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.SSAS_Predict_NBays_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.SSAS_Predict_NBays_sp
SELECT TOP 10 * FROM [dbo].[SSAS_Predict_NBays] ORDER BY [DataID]
SELECT TOP 10 * FROM [dbo].[DRV_Predict] WHERE [Model]='NBays'
*****************************************************/

