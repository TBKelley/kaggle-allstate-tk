IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.DRV_Predict_Ensumble_LOAD_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.DRV_Predict_Ensumble_LOAD_sp
GO

/**************************************************
File: DRV_Predict_Ensumble_LOAD_sp.sql

Description: Predition of validation data based on Ensumble of probabilities 

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.DRV_Predict_Ensumble_LOAD_sp
AS
SET NOCOUNT ON -- Required for VBA

DECLARE @Ensumble TABLE
(
 [DataID] INT NOT NULL
,[Predicted] FLOAT NOT NULL
,[Probablity] FLOAT NOT NULL
,[Base] FLOAT NOT NULL
,[DTree] FLOAT NOT NULL
,[LogisticR] FLOAT NOT NULL
,[NBays] FLOAT NOT NULL
,[NNetwork] FLOAT NOT NULL
,[SVM] FLOAT NOT NULL
,[RandomForest] FLOAT NOT NULL
)

INSERT @Ensumble
EXEC [dbo].[DRV_Predict_PIVOT_Ensumble1_sp]

SELECT
 E.DataID
,[RAW_Data].[PassengerId]
,[RAW_Data].[Actual]
,'=IF(RC[-1]<>RC[+1], IF(RC[+1]="", "", "FAIL"), "")' AS [Match]
,'=IF(RC[1]>=MinProbability,1,IF(RC[1]<=1-MinProbability,0,""))' AS [Predicted]
,'=(RC[+1] + RC[+2] + RC[+3] + RC[+4] + RC[+5] + RC[+6] + RC[+7])/7.0' AS [Probablity]
,E.Base
,E.DTree
,E.LogisticR
,E.NBays
,E.NNetwork
,E.SVM
,E.RandomForest
FROM @Ensumble E 
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[DataID] = E.DataID
WHERE [RAW_Data].[DataType] = 2 -- Cross Validation
ORDER BY E.DataID

GO

GRANT EXEC, VIEW DEFINITION ON dbo.DRV_Predict_Ensumble_LOAD_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.DRV_Predict_Ensumble_LOAD_sp
*****************************************************/

