local function complex_redis_command(key, value)
    local dict = {}
    dict[key] = value
    return dict
end
