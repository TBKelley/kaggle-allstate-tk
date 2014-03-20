IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.DRV_Predict_PIVOT_Ensumble1_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.DRV_Predict_PIVOT_Ensumble1_sp
GO

/**************************************************
File: DRV_Predict_PIVOT_Ensumble1_sp.sql

Description: Build Ensumble Pivot Table

Returns
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

History:
2014-01-03    Create  Created
**************************************************/
CREATE PROCEDURE dbo.DRV_Predict_PIVOT_Ensumble1_sp
AS
SET NOCOUNT ON -- Required for VBA

SELECT *
INTO #PivotTable
FROM
(
    SELECT [RAW_Data].[DataID], [DRV_Predict].[Model], [DRV_Predict].[Probablity]
    FROM [dbo].[RAW_Data]
    JOIN [dbo].[DRV_Predict]
      ON [DRV_Predict].[DataID] = [RAW_Data].[DataID]
) AS T
PIVOT
(
	MAX([Probablity]) FOR [Model] IN ([Base], [DTree], [LogisticR], [NBays], [NNetwork], [SVM], [DecisionTree], [RandomForest])
) AS PivotTable

SELECT
 [DataID]
,([Base] + [DTree] + [LogisticR] + [NBays] + [NNetwork] + [SVM] + [DecisionTree] + [RandomForest])/8.0 AS [Probablity]
,[Base]
,[DTree]
,[LogisticR]
,[NBays]
,[NNetwork]
,[SVM]
,[DecisionTree]
,[RandomForest]
INTO #Probablity
FROM #PivotTable
ORDER BY [DataID]

--SELECT * FROM #Probablity

SELECT
 [DataID]
,CASE WHEN [Probablity] >= 0.5 THEN 1 ELSE 0 END AS [Predicted]
,[Probablity]
,[Base]
,[DTree]
,[LogisticR]
,[NBays]
,[NNetwork]
,[SVM]
,[DecisionTree]
,[RandomForest]
FROM #Probablity
ORDER BY [DataID]

DROP TABLE #PivotTable
DROP TABLE #Probablity

GO

GRANT EXEC, VIEW DEFINITION ON dbo.DRV_Predict_PIVOT_Ensumble1_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.DRV_Predict_PIVOT_Ensumble1_sp
*****************************************************/

