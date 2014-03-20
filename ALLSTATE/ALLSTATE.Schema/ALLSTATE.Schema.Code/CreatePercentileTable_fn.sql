IF (EXISTS (SELECT * FROM sysobjects WHERE name = 'CreatePercentileTable_fn' AND type = 'TF'))
    DROP FUNCTION dbo.CreatePercentileTable_fn
GO

/**************************************************
File: CreatePercentileTable_fn.sql

Description: Create a dbo.BucketsTable based on @ValueTable percentiles

Parameters:
@ValueTable : Values to be converted into percentile buckets 
@Buckets    : Number of percentile buckets

Return value: TABLE of type dbo.BucketsTable

USAGE:
    DECLARE @ValueTable dbo.ValueTable
    DECLARE @Buckets dbo.BucketsTable
    DECLARE @Bucket FLOAT

    INSERT @ValueTable
    SELECT Value
    FROM Table

    --SET @Buckets = dbo.CreatePercentileTable_fn(@ValueTable, Buckets)
    INSERT @Buckets
    SELECT * FROM dbo.CreatePercentileTable_fn(@ValueTable, 10)

    SET @Bucket = dbo.Bucket_fn(@Buckets, 23.4)

History:
2014-01-08    TrKelley  Created
**************************************************/
CREATE FUNCTION dbo.CreatePercentileTable_fn(@ValueTable dbo.ValueTable READONLY, @Buckets INT)
RETURNS @ReturnTable TABLE
(
     MinValue FLOAT NOT NULL -- <= X
    ,MaxValue FLOAT NOT NULL -- X <
    ,MidValue FLOAT NOT NULL -- Middle of bucket range. AVG or MEDIAN
    ,Records INT NULL
)
AS
 BEGIN
    DECLARE @MinValue FLOAT
    DECLARE @MaxValue FLOAT   
    DECLARE @BucketSize FLOAT
    DECLARE @Records INT

    SELECT @MinValue=MIN(X), @MaxValue=MAX(X), @Records=COUNT(*) FROM @ValueTable
    SET @BucketSize = CAST(@Records AS FLOAT)/CAST(@Buckets AS FLOAT)

    DECLARE  @X  FLOAT

    DECLARE Record_cursor CURSOR FORWARD_ONLY READ_ONLY FOR
    SELECT X
    FROM @ValueTable
    ORDER BY X

    OPEN Record_cursor

    FETCH NEXT FROM Record_cursor
    INTO @X

    DECLARE @Record INT
    DECLARE @BucketRecords INT
    DECLARE @RecordBucketStart FLOAT
    DECLARE @RecordBucketEnd FLOAT
    DECLARE @Min FLOAT
    DECLARE @Max FLOAT
    DECLARE @Mid FLOAT
    SET @Record = 0
    SET @RecordBucketStart = 0
    SET @RecordBucketEnd = 0
    INSERT @ReturnTable(MinValue, MaxValue, MidValue) VALUES ('-1.79E+308' , @MinValue, @MinValue)
    WHILE (@@FETCH_STATUS = 0)
    BEGIN
        SET @RecordBucketEnd = @RecordBucketEnd + @BucketSize
        SET @Min = @X
        SET @Max = @X
        SET @BucketRecords = 0
        WHILE (@@FETCH_STATUS = 0
          AND @Record < @RecordBucketEnd)
        BEGIN
            -- Process Record
            SET @Record = @Record + 1
            FETCH NEXT FROM Record_cursor
            INTO @X

            IF (@@FETCH_STATUS = 0
            AND @Record < @RecordBucketEnd)
             BEGIN
                SET @Max = @X
                SET @BucketRecords =  @BucketRecords + 1
             END
        END
        SET @Mid = (@Max + @Min) * 0.5
        INSERT @ReturnTable(MinValue, MaxValue, MidValue, Records) VALUES (@Min, @Max, @Mid, @BucketRecords)
    END
    CLOSE Record_cursor
    DEALLOCATE Record_cursor
    INSERT @ReturnTable(MinValue, MaxValue, MidValue) VALUES (@MaxValue , '1.79E+308', @MaxValue)

    RETURN
 END
GO

GRANT SELECT, REFERENCES, VIEW DEFINITION ON dbo.CreatePercentileTable_fn TO PUBLIC
GO

/*****************************************************
-- UNIT CreatePercentileTable CASES
DECLARE @ValueTable dbo.ValueTable
DECLARE @Table dbo.BucketsTable

INSERT @ValueTable
SELECT [FareFLOAT]
FROM dbo.WRK_Data

INSERT @Table
SELECT * FROM dbo.CreatePercentileTable_fn(@ValueTable, 50)
SELECT * FROM @Table
*****************************************************/

