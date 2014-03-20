IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.DRV_Predict_Percepron_LOAD_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.DRV_Predict_Percepron_LOAD_sp
GO

/**************************************************
File: DRV_Predict_Percepron_LOAD_sp.sql

Description: Preditions of cross validation data from each model.
             Used as input to a Percepron model to determine weights
             for each model in the ensumble.

DESIGN: Return probabilities that may be pre-processed.

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.DRV_Predict_Percepron_LOAD_sp
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
,[DecisionTree] FLOAT NOT NULL
,[RandomForest] FLOAT NOT NULL
)

INSERT @Ensumble
EXEC [dbo].[DRV_Predict_PIVOT_Ensumble1_sp]

SELECT
 E.DataID
,[RAW_Data].[Actual]
,E.Base
,E.DTree
,E.LogisticR
,E.NBays
,E.NNetwork
,E.SVM
,E.DecisionTree
,E.RandomForest
,[RAW_Data].[DataType]
FROM @Ensumble E 
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[DataID] = E.DataID
ORDER BY E.DataID

GO

GRANT EXEC, VIEW DEFINITION ON dbo.DRV_Predict_Percepron_LOAD_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.DRV_Predict_Percepron_LOAD_sp
*****************************************************/

