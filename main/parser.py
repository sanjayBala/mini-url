import os
import redis

#counter_seq = 12345
class URLShortener():
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

    def dbConnect(self):
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

    def processUrl(self, original_url):
        """
            Returns original and encoded/shortened url as output
        """
        # global counter_seq
        red = self.dbConnect()
        print("ORIGINAL URL: " + str(original_url))
        if red.sismember('URL_SET', original_url):
            print("Same URL mapping already exists, let's find that...")
            # return the existing encoded url
            key_list = red.keys()
            for key in key_list:
                curr_val = red.get(key).decode('UTF-8')
                if curr_val == original_url:
                    print("Found Mapping: " + str(key) + " => " + str(curr_val) )
                    return key.decode('UTF-8')
            print("No Mapping found, something is wrong...")
            return None
        else:
            print("Adding the new URL to redis cache...")
            counter_seq = self.getAndUpdateCounter()
            encoded_url = self.encodeUrl(counter_seq)
            print("ENCODED URL: " + str(encoded_url))
            print("COUNTER VALUE: " + str(counter_seq))
            red.set(encoded_url, original_url)
            # add this to a global set for quick lookup
            red.sadd('URL_SET', original_url)
            return encoded_url

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
        red = self.dbConnect()
        curr_counter=0
        if 'counter_value' in red:
            curr_counter = int(red.get('counter_value').decode('UTF-8'))
            print("incrementing counter...")
            print("older value: " + str(curr_counter))
            red.set('counter_value', curr_counter + 1)
        else:
            red.set('counter_value', 14433)
        return curr_counter

    def listAll(self):
        """
            Lists all keys in redis db cache
        """
        red = self.dbConnect()
        return red.keys()
