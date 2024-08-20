box.cfg {
    listen = 3302,
    log_level = 5,
    memtx_memory = 512 * 1024 * 1024,
    replication = {
        'tarantool-cluster-shard2-1:3302',
        'tarantool-cluster-shard1-1:3301'
    },
    replication_timeout = 1.0
}
