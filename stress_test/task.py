import argparse
from py2neo import Graph

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--skip", type=int, required=True)
parser.add_argument("-l", "--limit", type=int, required=True)

args = parser.parse_args()


graph = Graph(
    password="12345678", host="10.9.3.209", port="7687"
)  # 7687: super big data


# # get all User_id:
res = graph.run(
    f"""
    MATCH (u:User)
    RETURN u.fb_id AS uid
    ORDER BY uid
    SKIP {args.skip} LIMIT {args.limit}
"""
)
all_uid = [node["uid"] for node in res.data()]


for uid in all_uid:
    res = graph.run(
        f"""
        MATCH (user1:User WHERE user1.fb_id='{uid}')-[r1:COMMENTED]->(post:Post)<-[r2:COMMENTED]-(user2:User)
        WHERE user1.fb_id < user2.fb_id // To avoid duplicate combinations
        WITH user1, user2, r1, r2,COLLECT(DISTINCT post) AS commonPosts
        RETURN user1, user2, r1, r2, commonPosts
    """
    )
