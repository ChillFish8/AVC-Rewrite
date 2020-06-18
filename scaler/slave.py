import sys

class Slave:
    starting_args = sys.argv
    CLUSTER_ID, SHARDS, TOTAL_SHARDS = int(starting_args[1]), int(starting_args[2]), int(starting_args[3])

    @classmethod
    def shard_ids_from_cluster(cls):
        return list(range(cls.SHARDS * cls.CLUSTER_ID, cls.SHARDS * cls.CLUSTER_ID + cls.SHARDS))
