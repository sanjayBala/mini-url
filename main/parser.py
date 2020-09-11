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
            r = redis.from_url(os.environ.get("REDIS_URL", "redis://h:pbdcc558025587326c87da83247eb8848b2eff3b66b33b95fccdce4453ad3a6c6@ec2-3-225-163-0.compute-1.amazonaws.com:18269"))
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
        if original_url in red:
            print("Same mapping exists already, let's use that...")
            # return the existing encoded url
            return red.get(original_url).decode('UTF-8')
        else:
            counter_seq = self.getCounter()
            encoded_url = self.encodeUrl(counter_seq)
            print("ENCODED URL: " + str(encoded_url))
            print("COUNTER VALUE: " + str(counter_seq))
            red.set(original_url, encoded_url)
            # add this to a global list for quick lookup
            red.lpush('GLOBAL_URLS', encoded_url)
            return encoded_url

    def getUrl(self, encoded_url):
        """
            Returns original and shortened url as output
            Invoked to redirect
        """
        red = self.dbConnect()
        encoded_url_list = red.get('GLOBAL_URLS')
        if encoded_url in encoded_url_list:
            print("URL Present!")
            return red.get(encoded_url).decode('UTF-8')
        print("Looks like this is a bad link!")
        return None

    def getCounter(self):
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
