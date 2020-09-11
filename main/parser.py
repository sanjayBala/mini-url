import os
import redis

class URLShortener():
    counter=12345

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

    def processUrl(self, original_url, counter):
        """
            Returns original and shortened url as output
        """
        red = self.dbConnect()
        encoded_url = self.encodeUrl(self.counter)
        print("COUNTER VALUE: " + str(counter))
        print("ORIGINAL URL: " + str(original_url))
        print("ENCODED URL: " + str(encoded_url))
        if encoded_url in red:
            return red.get(encoded_url), encoded_url
        else:
            # key is encoded url - value is original url
            red.set(encoded_url, original_url)
            print("incrementing counter...")
            counter = counter + 1
            return original_url, encoded_url

    def getUrl(self, encoded_url):
        """
            Returns original and shortened url as output
        """
        red = self.dbConnect()
        if encoded_url in red:
            print("URL Present!")
            return red.get(encoded_url).decode('UTF-8')
        return None

    def listAll(self):
        """
            Lists all keys in redis db cache
        """
        red = self.dbConnect()
        return red.keys()
