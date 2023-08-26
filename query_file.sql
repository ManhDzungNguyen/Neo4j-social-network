CREATE TABLE #temp(IdxCol BIGINT NOT NULL)
INSERT INTO #temp
(
IdxCol
)
SELECT DISTINCT TOP(20000) bd.IdxCol
FROM dbo.BenchmarkDetail bd WITH(NOLOCK) 
WHERE bd.BenchmarkId = @BenchmarkId
AND bd.SourceType = 1
{0}
{1}
SELECT TOP(1200000) a.id , a.idxcol
, sum(total_actor_post) total_actor_post
, SUM(total_comment) total_comment
, SUM(total_share) total_share
, SUM(total_reaction) total_reaction
FROM (
    SELECT f.FBId id, t.IdxCol idxcol, COUNT(*) total_actor_post, 0 total_comment, 0 total_share, 0 total_reaction
    FROM #temp t WITH(NOLOCK) 
    INNER JOIN dbo.FBFeeds f WITH(NOLOCK) ON f.IdxCol = t.IdxCol
    WHERE f.FBId > 0
    GROUP BY f.FBId, t.IdxCol
    UNION ALL

    SELECT c.FBId, t.IdxCol, 0 total_actor_post, COUNT(*) total_comment, 0 total_share, 0 total_reaction
    FROM #temp t WITH(NOLOCK) 
    INNER JOIN dbo.FBComments c WITH(NOLOCK) ON c.FBFeedIdxCol = t.IdxCol
    WHERE c.FBId > 0
    GROUP BY c.FBId  , t.IdxCol
    UNION ALL

    SELECT s.FBId, t.IdxCol, 0 total_actor_post, 0 total_comment, COUNT(*) total_share, 0 total_reaction
    FROM #temp t WITH(NOLOCK) 
    INNER JOIN dbo.FBFeeds f WITH(NOLOCK)  ON f.IdxCol = t.IdxCol
    INNER JOIN dbo.FBShares s WITH(NOLOCK) ON s.FBFeedId = f.FeedId
    WHERE s.FBId > 0
    GROUP BY s.FBId, t.IdxCol
    -- UNION ALL

    -- SELECT l.FBId, t.IdxCol, 0 total_actor_post, 0 total_comment, 0 total_share, COUNT(*) total_reaction
    -- FROM #temp t WITH(NOLOCK) 
    -- INNER JOIN dbo.FBFeeds f WITH(NOLOCK) ON f.IdxCol = t.IdxCol
    -- INNER JOIN dbo.FBLikes l WITH(NOLOCK) ON l.FBFeedId =  f.FeedId
    -- GROUP BY l.FBId  , t.IdxCol
) a
GROUP BY a.id , a.idxcol
DROP TABLE #temp;