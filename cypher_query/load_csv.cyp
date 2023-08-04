LOAD CSV WITH HEADERS FROM 'file:///data_user_post_full.csv' AS row
CALL {
    WITH row
    MERGE (user:User {fb_id: row.fb_id})
    MERGE (post:Post {post_id: row.post_id})

    FOREACH(ignoreMe IN CASE WHEN toInteger(row.total_actor_post) > 0 THEN [1] ELSE [] END |
        CREATE (user)-[:POST]->(post)
    )

    FOREACH(ignoreMe IN CASE WHEN toInteger(row.total_share) > 0 THEN [1] ELSE [] END |
        CREATE (user)-[:SHARED {total_share: toInteger(row.total_share)}]->(post)
    )

    FOREACH(ignoreMe IN CASE WHEN toInteger(row.total_reaction) > 0 THEN [1] ELSE [] END |
        CREATE (user)-[:REACTED {total_reaction: toInteger(row.total_reaction)}]->(post)
    )

    FOREACH(ignoreMe IN CASE WHEN toInteger(row.total_comment) > 0 THEN [1] ELSE [] END |
        CREATE (user)-[:COMMENTED {
            total_comment: toInteger(row.total_comment),
            first_cmt_time: datetime(row.first_cmt_time),
            last_cmt_time: datetime(row.last_cmt_time)
        }]->(post)
    )
} IN TRANSACTIONS OF 2000 ROWS;