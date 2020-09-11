import os
import collections
import redis

counter = collections.Counter(range(1, 100))

def encodeUrl(self, id):
    """
        Encodes and returns a base62 output
    """
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # base = 62
    base = len(characters)
    ret = []
    while id > 0:
        val = id % base
        ret.append(characters[val])
        id = id // base
    # reverse and return
    return "".join(ret[::-1])

def dbConnect():
    """
        Attempts a DB connection and returns the DB Object
    """
    r = 0
    try:
        r = redis.from_url(os.environ.get("REDIS_URL"))
        print("DB Connection seems okay!")
    except Exception as error:
        print ("Oops! An exception has occured:", error)
        print ("Exception TYPE:", type(error))
        r = None
    finally:
        return r

def processUrl(original_url):
    """
        Returns original and shortened url as output
    """
    red = dbConnect()
    if original_url in red:
        return original_url, red.get(original_url)
    else:
        encoded_url = encodeUrl(original_url, 1)
        red.set(original_url, encoded_url)
        return original_url, encoded_url