IF (EXISTS (SELECT * FROM sysobjects WHERE name = 'CreateBucketTable_fn' AND type = 'TF'))
    DROP FUNCTION dbo.CreateBucketTable_fn
GO

/**************************************************
File: CreateBucketTable_fn.sql

Description: Create a dbo.BucketsTable to be used with dbo.Buket_fn

Parameters:
@MinValue   : Minimum value 
@MaxValue   : Maximum value
@Buckets    : Number of buckets

Return value: TABLE of type dbo.BucketsTable

USAGE:
    DECLARE @Buckets dbo.BucketsTable
    DECLARE @Bucket FLOAT

    --SET @Buckets = dbo.CreateBucketTable_fn(MinValue, MaxValue, Buckets)
    INSERT @Buckets
    SELECT * FROM dbo.CreateBucketTable_fn(0.0, 100.0, 10)

    SET @Bucket = dbo.Bucket_fn(@Buckets, 23.4)

History:
2014-01-08    TrKelley  Created
**************************************************/
CREATE FUNCTION dbo.CreateBucketTable_fn(@MinValue FLOAT, @MaxValue FLOAT, @Buckets INT)
RETURNS @ReturnTable TABLE
(
     MinValue FLOAT NOT NULL -- <= X
    ,MaxValue FLOAT NOT NULL -- X <
    ,MidValue FLOAT NOT NULL -- Middle of bucket range. AVG or MEDIAN
    ,Records INT NULL
)
AS
 BEGIN
    DECLARE @BucketSize FLOAT
    SET @BucketSize = (@MaxValue - @MinValue)/CAST(@Buckets AS FLOAT)

    DECLARE @Min FLOAT
    DECLARE @Max FLOAT
    DECLARE @Mid FLOAT

    SET @Min = @MinValue
    INSERT @ReturnTable(MinValue, MaxValue, MidValue) VALUES ('-1.79E+308' , @MinValue, @MinValue)
    WHILE (@Min < @MaxValue)
     BEGIN
        SET @Max = @Min + @BucketSize
        SET @Mid = (@Min + @Max) * 0.5
        INSERT @ReturnTable(MinValue, MaxValue, MidValue) VALUES (@Min, @Max, @Mid)

        SET @Min = @Max
     END
    INSERT @ReturnTable(MinValue, MaxValue, MidValue) VALUES (@MaxValue , '1.79E+308', @MaxValue)

    RETURN
 END
GO

GRANT SELECT, REFERENCES, VIEW DEFINITION ON dbo.CreateBucketTable_fn TO PUBLIC
GO

/*****************************************************
-- UNIT CreateBucketTable CASES
DECLARE @Table dbo.BucketsTable
INSERT @Table
SELECT * FROM dbo.CreateBucketTable_fn(0.0, 100.0, 10)
SELECT * FROM @Table

SELECT * FROM dbo.CreateBucketTable_fn(0.0, 100.0, 10)
*****************************************************/

