box.cfg({
    listen = 3300,
})

local routers = {
    [1] = 'tarantool-cluster-shard1-1:3301',
    [2] = 'tarantool-cluster-shard2-1:3302'
}

box.once('init', function()
    local space = box.schema.space.create('example_space_5', { if_not_exists = true })
    space:format({
        { name = 'key', type = 'string' },
        { name = 'json_data', type = 'string' }
    })
    space:create_index('primary', {
        type = 'TREE',
        parts = { 1, 'string' },
        if_not_exists = true
    })
end)

local function get_shard_id(key)
    return (key % #routers) + 1
end

local connections = {}
local function get_connection(shard_id)
    if not connections[shard_id] then
        connections[shard_id] = require('net.box').connect(routers[shard_id])
    end
    return connections[shard_id]
end

local function insert(key, value)
    local shard_id = get_shard_id(key)
    local connection = get_connection(shard_id)
    connection.space.example_space_5:insert({ key, value })
end

local function select(key)
    local shard_id = get_shard_id(key)
    local connection = get_connection(shard_id)
    return connection.space.example_space_5:get(key)
end

return {
    insert = insert,
    select = select
}
