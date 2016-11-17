#!/usr/bin/python
#-*-coding:utf-8-*-

"""
    After you run the project every time,the stats infomation in still in the redis database.

    Run this file can help you clear the stats in the redis database.
"""

import redis

# default values
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
STATS_KEY = 'image:stats'

def clear_stats():
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    server.delete(STATS_KEY)

if __name__ == "__main__":
    clear_stats()
