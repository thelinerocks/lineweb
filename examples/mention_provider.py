#!/bin/bash

import redis
import random
import time
import json
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
    hashtag1 = "mentions-#icupper"
    hashtag2 = "mentions-#iclower"
    count = 0

    while True:
        time.sleep(1)
        mention = {"linetag": "icupper", "user_name": "user{}".format(count), "message": "This is great!!! {}", "profile_pic_url": "https://vignette.wikia.nocookie.net/simpsons/images/d/df/Bart-gangster-psd4202.png/revision/latest?cb=20100720001226"}
        count += 1
        if r.llen(hashtag1) < 5:
            r.lpush(hashtag1, json.dumps(mention))
        mention = {"linetag": "iclower", "user_name": "user{}".format(count), "message": "This is great!!! {}", "profile_pic_url": "https://vignette.wikia.nocookie.net/simpsons/images/d/df/Bart-gangster-psd4202.png/revision/latest?cb=20100720001226"}
        count += 1
        if r.llen(hashtag2) < 5:
            r.lpush(hashtag2, json.dumps(mention))
        logger.debug("Sent datapoints - q length %d", r.llen(hashtag2))
