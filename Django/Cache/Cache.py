"""
🧠 What is Cache?

Cache is a temporary storage layer that keeps frequently accessed data in a location that is faster to read from than the original source (like a database, API, or file system).

Purpose: Speed up data retrieval and reduce repeated expensive operations.

Example: Instead of querying the database every time for the same user info, you store it in cache and fetch it quickly.
"""


"""
⚡ Example:

Without cache:

Request → Database → Response
"""


"""
With cache:

Request → Cache (fast) → Response
"""

"""
If cache doesn’t have the data, fetch from DB and store it in cache for next time.

This improves performance dramatically for frequently requested data.

🏗️ Cache System

A cache system is the infrastructure that manages cache. It usually includes:

Storage layer: Where cached data is stored.

In-memory: Redis, Memcached (fastest)

File-based: local file system

Browser cache (for front-end)

Expiration / TTL (Time-to-Live): How long cached data should stay before being refreshed.

Eviction policies: How the system decides what data to remove when space is full:

LRU (Least Recently Used)

FIFO (First In First Out)

LFU (Least Frequently Used)
"""


from django.core.cache import cache

# Store data in cache for 5 minutes
cache.set('my_key', 'my_value', 300)

# Get data from cache
value = cache.get('my_key')
print(value)  # Output: 'my_value'


"""
Cache = Temporary fast storage for frequently used data.

Cache system = The mechanism (like Redis, Memcached) that stores, retrieves, and manages cached data.

Improves performance, reduces database load, and speeds up web apps.
"""