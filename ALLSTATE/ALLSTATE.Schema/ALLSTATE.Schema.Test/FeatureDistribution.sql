SELECT
 AVG(CAST([Actual] AS FLOAT)) AS [Survive%]
,COUNT(*) AS [Count]
FROM [dbo].[WRK_Train_vw]
WHERE [DataType] IN (1,2)

SELECT
 [SexINT]
,AVG(CAST([Actual] AS FLOAT)) AS [Survive%]
,COUNT(*) AS [Count]
FROM [dbo].[WRK_Train_vw]
WHERE [DataType] IN (1,2)
GROUP BY [SexINT]
ORDER BY [SexINT]

SELECT
 [SalutationHash]
,AVG(CAST([Actual] AS FLOAT)) AS [Survive%]
,COUNT(*) AS [Count]
FROM [dbo].[WRK_Train_vw]
WHERE [DataType] IN (1,2)
GROUP BY [SalutationHash]
ORDER BY [SalutationHash]

SELECT
 [DeckHash]
,[SexINT]
,AVG(CAST([Actual] AS FLOAT)) AS [Survive%]
,COUNT(*) AS [Count]
FROM [dbo].[WRK_Train_vw]
WHERE [DataType] IN (1,2)
GROUP BY [DeckHash], [SexINT]
ORDER BY [DeckHash], [SexINT]

SELECT
 [DeptCodeHash]
,[SexINT]
,AVG(CAST([Actual] AS FLOAT)) AS [Survive%]
,COUNT(*) AS [Count]
FROM [dbo].[WRK_Train_vw]
WHERE [DataType] IN (1,2)
GROUP BY [DeptCodeHash], [SexINT]
ORDER BY [DeptCodeHash], [SexINT]