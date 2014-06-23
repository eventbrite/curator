# Curator

A python helper to make it easier to work with lua scripts in redis.

__Inspired by/python port of Shopify's [wolverine](https://github.com/Shopify/wolverine).__

## Usage

1) Ensure you have redis 2.6 or higher installed:

```
redis-server -v
```

2) Install curator:

```
pip install https://github.com/mhahn/curator.git@0.0.1
```

3) Add your lua scripts to a directory, ie:

```lua
-- app/lua_scripts/util/mexists.lua
local exists = {}
local existence
for _, key in ipairs(KEYS) do
  table.insert(exists, redis.call('exists', key))
end
return exists
```

4) Configure and call Curator in your code:

```python
from redis import Redis
from curator import Curator

# this should happen when you start your server
curator = Curator(
    package='app',
    scripts_dir='lua_scripts',
    redis_client=Redis(),
)

print curator.util.mexists(keys=['key1', 'key2', 'key3'])
# [0, 1, 0]
```

Methods are available on `curator` based on the directory structure of the `scripts_dir`.

#### Nested Lua Scripts

For lua scripts with shared code, Curator supports [jinja](http://jinja.pocoo.org/) templating.

If your app has lua scripts at

- `app/lua_scripts/do_something.lua`
- `app/lua_scripts/do_something_else.lua`

that both have shared lua code, you can factor it out into a lua "partial":

- `app/lua_scripts/shared/_common.lua`

```lua
-- app/lua_scripts/shared/_common.lua
local function complex_redis_command(key, value)
  local dict = {}
  dict[key] = value
end
```

```lua
-- app/lua_scripts/do_something.lua
{% include 'shared/_common.lua' %}
complex_redis_command("foo", "bar")
return true
```

```lua
-- app/lua_scripts/do_something_else.lua
{% include 'shared/_common.lua' %}
complex_redis_command("bar", "baz")
return false
```

- partials are loaded relative to the `scripts_dir` location you instantiate Curator with.

## More information

For more information on scripting redis with lua, refer to redis' excellent documentation: http://redis.io/commands/eval
