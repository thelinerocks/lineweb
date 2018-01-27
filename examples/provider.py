#!/bin/bash

import redis
import random
import time
import logging

logger = logging.getLogger("provider")

if __name__=="__main__":
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    val = 0
    hashtag1 = "points-#icupper"
    hashtag2 = "points-#iclower"

    while True:
        time.sleep(0.05)
        val = random.random()*5
        r.lpush(hashtag1, val)
        if r.llen(hashtag1) > 1000:
            r.rpop(hashtag1)

        val = random.random()*5
        r.lpush(hashtag2, val)
        if r.llen(hashtag2) > 1000:
            r.rpop(hashtag2)
        logger.debug("Sent datapoints - q length %d", r.llen(hashtag2))
