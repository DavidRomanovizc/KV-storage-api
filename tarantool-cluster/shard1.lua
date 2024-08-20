box.cfg {
    listen = 3301,
    log_level = 5,
    memtx_memory = 512 * 1024 * 1024,
    replication = {
        'tarantool-cluster-shard1-1:3301',
        'tarantool-cluster-shard2-1:3302',
    },
    replication_timeout = 1.0
}
