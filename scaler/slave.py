import sys

class Slave:
    def __init__(self):
        starting_args = sys.argv
        self.CLUSTER_ID, self.SHARDS, self.TOTAL_SHARDS = \
            int(starting_args[1]), int(starting_args[2]), int(starting_args[3])

    def shard_ids_from_cluster(self):
        return list(range(self.SHARDS * self.CLUSTER_ID, self.SHARDS * self.CLUSTER_ID + self.SHARDS))
