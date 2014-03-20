IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.DRV_Predict_INSERT_Ensumble1_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.DRV_Predict_INSERT_Ensumble1_sp
GO

/**************************************************
File: DRV_Predict_INSERT_Ensumble1_sp.sql

Description: Predition of validation data based on Ensumble of probabilities 

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.DRV_Predict_INSERT_Ensumble1_sp
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

DELETE [dbo].[DRV_Predict] WHERE [Model] = 'Ensumble1'

INSERT @Ensumble
EXEC [dbo].[DRV_Predict_PIVOT_Ensumble1_sp]

INSERT [dbo].[DRV_Predict] ([Model], [DataID], [Predicted], [Probablity])
SELECT 
 'Ensumble1' AS [Model]
,E.[DataID]
,E.[Predicted]
,E.[Probablity]
FROM @Ensumble E
JOIN [dbo].[RAW_Data]
  ON [RAW_Data].[DataID] = E.[DataID]
ORDER BY E.[DataID]

GO

GRANT EXEC, VIEW DEFINITION ON dbo.DRV_Predict_INSERT_Ensumble1_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.DRV_Predict_INSERT_Ensumble1_sp
SELECT * FROM DRV_Predict_vw WHERE [Model] = 'Ensumble1'
*****************************************************/

