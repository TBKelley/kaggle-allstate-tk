IF  (EXISTS (SELECT * FROM sys.objects WHERE OBJECT_ID = OBJECT_ID('dbo.RAW_FareAnalysis_PIVOT_sp') AND type in ('P', 'PC')))
    DROP PROCEDURE dbo.RAW_FareAnalysis_PIVOT_sp
GO

/**************************************************
File: RAW_FareAnalysis_PIVOT_sp.sql

Description: Correlation Between Fare Price and Survival Rate

NOTE: Used to generate date for CorrelationBetweenFarePriceAndSurvivalRate.xlsx

History:
2014-01-09    Create  Created
**************************************************/
CREATE PROCEDURE dbo.RAW_FareAnalysis_PIVOT_sp
    @Buckets INT = 20
AS
SET NOCOUNT ON

DECLARE @ValueTableMale dbo.ValueTable
DECLARE @BucketsTableMale dbo.BucketsTable
DECLARE @ValueTableFemale dbo.ValueTable
DECLARE @BucketsTableFemale dbo.BucketsTable
DECLARE @Bucket FLOAT
DECLARE @X FLOAT

INSERT @ValueTableMale
SELECT [WRK_Data].[FareFLOAT]
FROM [dbo].[WRK_Data]
JOIN [dbo].[RAW_Data]
    ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
    AND [RAW_Data].[DataType] IN (1, 2)
WHERE [WRK_Data].[FareFLOAT] > 0.5
  AND [RAW_Data].[Sex] = 'Male'
ORDER BY [WRK_Data].[FareFLOAT]

INSERT @BucketsTableMale
SELECT * FROM dbo.CreatePercentileTable_fn(@ValueTableMale,  @Buckets)

INSERT @ValueTableFemale
SELECT [WRK_Data].[FareFLOAT]
FROM [dbo].[WRK_Data]
JOIN [dbo].[RAW_Data]
    ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
    AND [RAW_Data].[DataType] IN (1, 2)
WHERE [WRK_Data].[FareFLOAT] > 0.5
  AND [RAW_Data].[Sex] = 'Female'
ORDER BY [WRK_Data].[FareFLOAT]

INSERT @BucketsTableFemale
SELECT * FROM dbo.CreatePercentileTable_fn(@ValueTableFemale,  @Buckets)

-- SELECT MinValue, MaxValue, MidValue, Records FROM @BucketsTable

SELECT *
FROM
(
    SELECT
     dbo.Bucket_fn(@BucketsTableMale, [WRK_Data].[FareFLOAT]) AS [Fare]
    ,'M Rate' AS [ColumnName]
    ,AVG(CAST([RAW_Data].[Actual] AS FLOAT)) AS [Value]
    FROM [dbo].[WRK_Data]
    JOIN [dbo].[RAW_Data]
      ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
     AND [RAW_Data].[DataType] IN (1, 2)
    WHERE [WRK_Data].[FareFLOAT] > 0.5
      AND [RAW_Data].[Sex] = 'Male'
    GROUP BY dbo.Bucket_fn(@BucketsTableMale, [WRK_Data].[FareFLOAT])
    UNION ALL
    SELECT
     dbo.Bucket_fn(@BucketsTableMale, [WRK_Data].[FareFLOAT]) AS [Fare]
    ,'M Size' AS [ColumnName]
    ,COUNT(*) AS  [Value]
    FROM [dbo].[WRK_Data]
    JOIN [dbo].[RAW_Data]
      ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
     AND [RAW_Data].[DataType] IN (1, 2)
    WHERE [WRK_Data].[FareFLOAT] > 0.5
      AND [RAW_Data].[Sex] = 'Male'
    GROUP BY dbo.Bucket_fn(@BucketsTableMale, [WRK_Data].[FareFLOAT])
    UNION ALL
    SELECT
     dbo.Bucket_fn(@BucketsTableFemale, [WRK_Data].[FareFLOAT]) AS [Fare]
    ,'F Rate' AS [ColumnName]
    ,AVG(CAST([RAW_Data].[Actual] AS FLOAT)) AS [Value]
    FROM [dbo].[WRK_Data]
    JOIN [dbo].[RAW_Data]
      ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
     AND [RAW_Data].[DataType] IN (1, 2)
    WHERE [WRK_Data].[FareFLOAT] > 0.5
      AND [RAW_Data].[Sex] = 'Female'
    GROUP BY dbo.Bucket_fn(@BucketsTableFemale, [WRK_Data].[FareFLOAT])
    UNION ALL
    SELECT
     dbo.Bucket_fn(@BucketsTableFemale, [WRK_Data].[FareFLOAT]) AS [Fare]
    ,'F Size' AS [ColumnName]
    ,COUNT(*) AS  [Value]
    FROM [dbo].[WRK_Data]
    JOIN [dbo].[RAW_Data]
      ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
     AND [RAW_Data].[DataType] IN (1, 2)
    WHERE [WRK_Data].[FareFLOAT] > 0.5
      AND [RAW_Data].[Sex] = 'Female'
    GROUP BY dbo.Bucket_fn(@BucketsTableFemale, [WRK_Data].[FareFLOAT])
) AS T
PIVOT
(
	AVG([Value]) FOR [ColumnName] IN ([M Rate], [M Size], [F Rate], [F Size])
) AS PivotTable

GO

GRANT EXEC, VIEW DEFINITION ON dbo.RAW_FareAnalysis_PIVOT_sp TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
EXEC dbo.RAW_FareAnalysis_PIVOT_sp
*****************************************************/

