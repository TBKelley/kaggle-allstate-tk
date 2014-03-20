/**************************************************
File: 05_AddTypes.sql

Description: Add User Defined TYPE

Used with
    DECLARE @Buckets dbo.BucketsTable
    DECLARE @Bucket FLOAT
    SET @Buckets = dbo.CreateBucketTable_fn(MinValue, MaxValue, Buckets)
    SET @Bucket = dbo.Bucket_fn(@Buckets, 23.4)

History:
2014-01-08 Trevor      Created
*************************************************/
PRINT 'Add User Defined TYPE'
--DROP TYPE [dbo].[BucketsTable]
CREATE TYPE dbo.BucketsTable AS
TABLE
(
     MinValue FLOAT NOT NULL -- <= X
    ,MaxValue FLOAT NOT NULL -- X <
    ,MidValue FLOAT NOT NULL -- Middle of bucket range. AVG or MEDIAN
    ,Records INT NULL        -- Used by Percentile buckets
)
GO

--DROP TYPE [dbo].[ValueTable]
CREATE TYPE dbo.ValueTable AS
TABLE
(
     X FLOAT NOT NULL
)
GO