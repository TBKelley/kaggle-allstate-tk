IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.SSAS_Predict_Ensemble_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.SSAS_Predict_Ensemble_sp
GO

/**************************************************
File: SSAS_Predict_Ensemble_sp.sql

Description: Create predictive table SSAS_Predict_Ensemble

RMSE=0.61+/-0.01 10%:>1.64%

History:
2013-11-01    TrKelley  Created
**************************************************/
CREATE PROCEDURE dbo.SSAS_Predict_Ensemble_sp
AS
DECLARE @Model VARCHAR(50)
SET @Model = 'Ensemble'

SET NOCOUNT ON

IF (EXISTS (SELECT * FROM sysobjects WHERE id = OBJECT_ID('dbo.SSAS_Predict_Ensemble') AND OBJECTPROPERTY(id, 'IsUserTable') = 1))
    DROP TABLE dbo.[SSAS_Predict_Ensemble]

EXEC [dbo].[SSAS_Predict_DTree_sp]
EXEC [dbo].[SSAS_Predict_LogisticR_sp]
EXEC [dbo].[SSAS_Predict_NBays_sp]
EXEC [dbo].[SSAS_Predict_NNetwork_sp]

DECLARE @SSAS_Predict_Ensemble TABLE 
(
	 [DataID] INT NOT NULL
    ,[Model] VARCHAR(50) NOT NULL
	,[Predicted] BIT  NOT NULL
	,[Probablity] FLOAT  NOT NULL
	,[ProbablityAdj] FLOAT  NOT NULL
    ,[Weight] FLOAT  NOT NULL
)

INSERT @SSAS_Predict_Ensemble (DataID, Model, Predicted, Probablity, ProbablityAdj, [Weight])
SELECT
 [DataID]
,'DTree' AS [Model]
,[Predicted]
,[Probablity]
,[ProbablityAdj]
,0.20 AS  [Weight]
FROM [dbo].[SSAS_Predict_DTree]
UNION
SELECT
 [DataID]
,'LogisticR' AS [Model]
,[Predicted]
,[Probablity]
,[ProbablityAdj]
,0.20 AS  [Weight]
FROM [dbo].[SSAS_Predict_LogisticR]
UNION
SELECT
 [DataID]
,'NBays' AS [Model]
,[Predicted]
,[Probablity]
,[ProbablityAdj]
,0.20 AS  [Weight]
FROM [dbo].[SSAS_Predict_NBays]
UNION
SELECT
 [DataID]
,'NNetwork' AS [Model]
,[Predicted]
,[Probablity]
,[ProbablityAdj]
,0.20 AS  [Weight]
FROM [dbo].[SSAS_Predict_NNetwork]

SELECT
 [DataID]
,[Model]
,[Predicted]
,[Probablity]
,[ProbablityAdj]
,[Weight]
FROM @SSAS_Predict_Ensemble
ORDER BY [DataID], [Model]

SELECT 
 [DataID]
,CASE WHEN SUM([Predicted]*[Weight]) >= 0.5 THEN 1 ELSE 0 END AS [Predicted]
,SUM([Probablity]*[Weight]) AS [Probablity]
,SUM([ProbablityAdj]*[Weight]) AS [ProbablityAdj]
INTO [dbo].[SSAS_Predict_Ensemble]
FROM @SSAS_Predict_Ensemble
GROUP BY [DataID]
ORDER BY [DataID]

DELETE [dbo].[DRV_Predict] WHERE [Model] = @Model

INSERT [dbo].[DRV_Predict] ([Model], [DataID], [Predicted], [Probablity])
SELECT
 @Model AS [Model]
,[DataID]
,[Predicted]
,[Probablity]
FROM [dbo].[SSAS_Predict_Ensemble]
ORDER BY [DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.SSAS_Predict_Ensemble_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.SSAS_Predict_Ensemble_sp
SELECT TOP 10 * FROM [dbo].[SSAS_Predict_Ensemble] ORDER BY [DataID]
SELECT TOP 10 * FROM [dbo].[DRV_Predict] WHERE [Model]='Ensemble'
*****************************************************/
