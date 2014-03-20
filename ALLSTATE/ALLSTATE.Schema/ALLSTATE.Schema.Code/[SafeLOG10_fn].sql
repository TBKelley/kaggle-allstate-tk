IF (EXISTS (SELECT * FROM sysobjects WHERE name = 'SafeLOG10_fn' AND type = 'FN'))
    DROP FUNCTION dbo.SafeLOG10_fn
GO

/**************************************************
File: [SafeLOG10_fn].sql

Description: Safe LOG() function for values that are 0...n

Parameters:
@Value    : Value

Return value: LOG10(@Value) or 0.0 if @Value = 0

History:
3013-10-10    TrKelley  Created
**************************************************/
CREATE FUNCTION dbo.SafeLOG10_fn(@Value FLOAT)
RETURNS FLOAT
AS
 BEGIN
    DECLARE @Return FLOAT
	IF (@Value < 1.0)
		SET @Return = 1.0
	ELSE
		SET @Return = LOG10(@Value)

    RETURN(@Return)
 END
GO

GRANT EXECUTE, REFERENCES, VIEW DEFINITION ON dbo.SafeLOG10_fn TO PUBLIC
GO

/*****************************************************
-- UNIT TEST CASES
SELECT dbo.SafeLOG10_fn(-1.0), '0.0'
SELECT dbo.SafeLOG10_fn(0), '0.0'
SELECT dbo.SafeLOG10_fn(1), '0'
SELECT dbo.SafeLOG10_fn(10), '1'
SELECT dbo.SafeLOG10_fn(100), '2'
SELECT dbo.SafeLOG10_fn('1000.0'), '3'
*****************************************************/

