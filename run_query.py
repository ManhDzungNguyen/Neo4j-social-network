from function import NeoAdapter
import time

neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")
start_time = time.time()


res = neo.run_query("""     
    CALL gds.louvain.write('user-icp', {
        writeProperty: 'louvain_cid',
        minCommunitySize: 5,
        relationshipWeightProperty: 'weight',
        maxLevels: 10
    })
    YIELD communityCount, modularity, modularities;
""")


print(res)
print(f"runtime: {time.time() - start_time}")