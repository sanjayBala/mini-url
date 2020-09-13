import os
import redis
from datetime import timedelta

days_to_live=7

class URLShortener():
    def dbConnect(self):
        """
            Attempts a Redis DB connection and returns the DB Object
        """
        r = redis.StrictRedis()
        try:
            r = redis.from_url(os.environ.get("REDIS_URL"))
            print("DB Connection seems okay!")
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            r = None
        finally:
            return r

    def shortURLToId(self, shortURL): 
        """
            Converts short URL to an ID
        """
        id = 0
        for i in shortURL: 
            val_i = ord(i) 
            if(val_i >= ord('a') and val_i <= ord('z')): 
                id = id*62 + val_i - ord('a') 
            elif(val_i >= ord('A') and val_i <= ord('Z')): 
                id = id*62 + val_i - ord('Z') + 26
            else: 
                id = id*62 + val_i - ord('0') + 52
        return id

    def encodeUrl(self, id):
        """
            Converts ID to a short URL
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

    def processUrl(self, original_url):
        """
            Returns original and encoded/shortened url as output
        """
        red = self.dbConnect()
        original_url=str(original_url)
        print("ORIGINAL URL: " + original_url)
        # check set to see if it is an existing url
        if red.sismember('URL_SET', original_url):
            print("Same URL mapping already exists, let's find that...")
            # return the existing url
            for key in red.scan_iter():
                if key.decode('utf-8') not in ['URL_SET', 'counter_value']:
                    print("Checking Key: " + str(key))
                    curr_val = red.get(key).decode('UTF-8')
                    print("Checking Value: " + str(curr_val))
                    if curr_val == original_url:
                        print("Found Mapping: " + str(key) + " => " + str(curr_val) )
                        return key.decode('UTF-8'), red.ttl(key)
            print("No Mapping found, something is wrong...")
            print("Possibly a manual deletion")
            print("Adding the URL mapping again...")
        # if not found or if it is a new url - do the following
        # add to cache, update counter
        print("Adding the new URL to redis cache...")
        counter_seq = self.getAndUpdateCounter()
        encoded_url = self.encodeUrl(counter_seq)
        print("ENCODED URL: " + str(encoded_url))
        print("NEW COUNTER VALUE: " + str(counter_seq))
        red.set(encoded_url, original_url)
        
        # adding an expiry
        expiry_time = timedelta(days=days_to_live)
        print("Setting an expiry of " + str(expiry_time.days) + " days for the URL.")
        red.expire(encoded_url, expiry_time)
        # add this to a global set for quick lookup
        red.sadd('URL_SET', original_url)
        return encoded_url, red.ttl(encoded_url)

    def redirectUrl(self, encoded_url):
        """
            Returns original and shortened url as output
            Invoked to redirect
        """
        red = self.dbConnect()
        if red.exists(encoded_url):
            print("This looks like a valid short URL")
            return str(red.get(encoded_url).decode('UTF-8'))
        else:
            print("This is not a valid short URL")
            return None

    def getCounter(self):
        red = self.dbConnect()
        return int(red.get('counter_value').decode('UTF-8'))

    def getAndUpdateCounter(self):
        """
            Returns the counter and increments by 1
        """
        red = self.dbConnect()
        curr_counter=0
        if 'counter_value' in red:
            curr_counter = int(red.get('counter_value').decode('UTF-8'))
            print("incrementing counter...")
            print("older value: " + str(curr_counter))
            red.set('counter_value', curr_counter + 1)
        else:
            # just an arbitrary value
            red.set('counter_value', 14433)
        return curr_counter

    def listAll(self):
        """
            Lists all keys in redis db cache
        """
        red = self.dbConnect()
        return red.keys()
