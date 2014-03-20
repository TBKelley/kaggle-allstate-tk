IF (EXISTS (SELECT * FROM sysobjects WHERE name = 'Bucket_fn' AND type = 'FN'))
    DROP FUNCTION dbo.Bucket_fn
GO

/**************************************************
File: Bucket_fn.sql

Description: Determine bucket of X

USAGE:
    DECLARE @Buckets dbo.BucketsTable
    DECLARE @Bucket FLOAT

    --SET @Buckets = dbo.CreateBucketTable_fn(MinValue, MaxValue, Buckets)
    INSERT @Buckets
    SELECT * FROM dbo.CreateBucketTable_fn(0.0, 100.0, 10)

    SET @Bucket = dbo.Bucket_fn(@Buckets, 23.4)

Parameters:
@Buckets    : Input dbo.BucketsTable
@X          : Value to be bucketed

Return value: MidValue of bucket range, or MinValue/MaxValue if out of range

Problems: Must return a FLOAT

History:
2014-01-08    TrKelley  Created
**************************************************/
CREATE FUNCTION dbo.Bucket_fn(@Buckets dbo.BucketsTable READONLY, @X FLOAT)
RETURNS FLOAT
AS
 BEGIN
    DECLARE @Return FLOAT
    SELECT TOP 1 @Return=T.MidValue
    FROM @Buckets T
    WHERE @X >= T.MinValue
    ORDER BY T.MinValue DESC, T.MaxValue

    RETURN(@Return)
 END
GO

GRANT EXECUTE, REFERENCES, VIEW DEFINITION ON dbo.Bucket_fn TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
DECLARE @Buckets dbo.BucketsTable
DECLARE @Bucket FLOAT
DECLARE @X FLOAT
SET @X = 23.4

INSERT @Buckets
SELECT * FROM dbo.CreateBucketTable_fn(0.0, 100.0, 10)

SELECT * FROM @Buckets ORDER BY MinValue

SET @Bucket = dbo.Bucket_fn(@Buckets, @X)
SELECT @X AS [X], @Bucket AS [Bucket Mid-point]
*****************************************************/


/*****************************************************
-- UNIT TEST CASES
DECLARE @ValueTable dbo.ValueTable
DECLARE @Buckets dbo.BucketsTable
DECLARE @Bucket FLOAT
DECLARE @X FLOAT
SET @X = 13

INSERT @ValueTable
SELECT [WRK_Data].[FareFLOAT]
FROM [dbo].[WRK_Data]
JOIN [dbo].[RAW_Data]
    ON [RAW_Data].[DataID] = [WRK_Data].[DataID]
    AND [RAW_Data].[DataType] IN (1, 2)
WHERE [WRK_Data].[FareFLOAT] > 0.5
  AND [RAW_Data].[Sex] = 'Male'
ORDER BY [WRK_Data].[FareFLOAT]

INSERT @Buckets
SELECT * FROM dbo.CreatePercentileTable_fn(@ValueTable, 50)

SELECT * FROM @Buckets ORDER BY MinValue

SELECT T.MinValue, T.MaxValue, T.MidValue
FROM @Buckets T
WHERE @X >= T.MinValue
ORDER BY T.MinValue DESC, T.MaxValue

SET @Bucket = dbo.Bucket_fn(@Buckets, @X)
SELECT @X AS [X], @Bucket AS [Bucket Mid-point]
*****************************************************/
