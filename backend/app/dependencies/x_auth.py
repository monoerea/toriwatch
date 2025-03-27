from tweepy import Client, OAuth1UserHandler, TweepyException, Stream, API
from tweepy.streaming import Stream
from tweepy import Stream
import keys
from numpy import array


class TwitterAuthenticator():
    def __init__(self, auth: OAuth1UserHandler = None, client: Client | API = None):
        self.auth = auth
        self.client = client

    def is_verified(self):
        if self.client and hasattr(self.client, '_get_oauth_1_authenticating_user_id'):
            return self.client._get_oauth_1_authenticating_user_id() is not None
        return self.auth and self.auth.access_token is not None

    def get_client(self)-> Client | None:
        if not self.is_verified():
            raise ValueError("Client is not authenticated. Call `verify` first.")
        if isinstance(self.client, Client):
            return self.client
        if not self.auth:
            raise ValueError("No authentication handler (auth) provided.")
        try:
            self.client = Client(access_token=self.auth.ACCESS_TOKEN, access_token_secret=self.auth.ACCESS_TOKEN_SECRET)
            return self.client
        except TweepyException  as e:
            print(f"Error creating Client: {e}")

    def get_api(self) -> API | None:
        if self.is_verified():
            return self.client
        if isinstance(self.client, API):
            return self.client
        if not self.auth:
            raise ValueError("No authentication handler (auth) provided.")
        try:
            self.client = API(auth=self.auth)
            return self.client
        except TweepyException  as e:
            print(f"Error creating Client: {e}")
    def get_auth_url(self):
        if self.is_verified() == True:
            return
        if not self.auth:
            self.auth = OAuth1UserHandler(
                consumer_key=keys.CONSUMER_KEY,
                consumer_secret=keys.CONSUMER_SECRET
            )
        return self.auth.get_authorization_url()
    def verify(self, pin):
        if self.is_verified() == True:
            return
        if not self.auth:
            self.auth = OAuth1UserHandler(
                consumer_key=keys.CONSUMER_KEY,
                consumer_secret=keys.CONSUMER_SECRET
            )
        if pin:
            try:
                access_token, access_token_secret = self.auth.get_access_token(verifier=pin)
                self.auth.set_access_token(access_token, access_token_secret)
            except TweepyException as e:
                print(f"Error during verification: {e}")
        else:
            if not (self.auth.access_token and self.auth.access_token_secret):
                print("Error: PIN is required for verification.")


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self, twitter_autenticator):
        self.twitter_autenticator = twitter_autenticator

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.auth
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(Stream):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        #self.passed_users = data.id

    def on_data(self, data):
        try:
            self.getPredArray(data=data)
            #print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
    
    def count_UserFeatures(store):
        keys = ['statuses_count','default_profile','default_profile_image','verified','favourites_count','followers_count','friends_count','listed_count'] # make to madular
        userObj =[] #initialize dict
        for j in range(len(store)): # enumerate doesn't work as of now
            for i in keys:
                userObj.append(store[j].get(i))
        return userObj
    def to_numpy_array(myDict):
    #myDict = myDict.items()
        myDict = list(myDict)
        myArray = [array(myDict)]
        #myDict.flatten()
        print(myArray)
        return myArray
    def getPredArray(self, data):
        userData = self.getUser(requestJson = data)
        userFeats = self.count_UserFeatures(userData)
        userArray = self.to_numpy_array(userFeats)
        return  userArray

    

def input_verify(myClient):
    verfier = input("Enter verifier:")
    myClient.set_pin(pin=verfier)
    if myClient.isVerified() == True:
        return myClient

def createTwitterClient():
        myClient = TwitterClient()
        return myClient

def createClient(): # FULLY WORKING WITH RE-ENTER INPUT
    #create my Class
        myClient = TwitterClient() # also create a authObj TwtAuth in Class to get auth
        #method to get auth, passes the authObj method inside this method to get the url
        url = myClient.get_auth()
        #prints url
        print(url)

        #Input sample
        pin = input("Enter verifier:")

        #Calls a authObj verifier method, checks if verified and reassigns twt-client
        myClient.set_pin(pin=pin)
        if myClient.isVerified() == True:
            return myClient
        else:
            while myClient.isVerified() == False:
                prompt = input("Continue?")
                if prompt== 'Y':
                    if myClient.isVerified() == False:
                        input_verify(myClient)
                    
                else: # assign client with me or false
                    raise ValueError("Wrong input!")
                #result = myClient.get_by_screenName('monoerea')
        #dm = myClient.get_dm('duke_jijii')
        #print(dm)
        #result = myClient.get_by_screenName(screen_name='monoerea')
        #result = myClient.get_client()
                #print(result)
        '''while (myClient.isVerified() == False):
            verfier = input("Enter verifier:")
            myClient.set_verifier(verifier=verfier)
        else:'''
        
def test_get_me():
    myClient = createClient()
    myClient.get_client()
def adminTest():
        myClient = TwitterClient('monoerea')
        result = myClient.get_client()
        print(type(myClient.twitter_client))
        print(result)
def main():
       # hash_tag_list = ["donal trump", "hillary clinton", "barack obama", "bernie sanders"]
      #  fetched_tweets_filename = "tweets.txt"
    #createClient()
    #adminTest()
    test_get_me()
        #print(myClient.auth.auth) # retrieved
        #print(myClient.twitter_client) # retrieved
if __name__ == '__main__': 
    # Authenticate using config.py and connect to Twitter Streaming API.
    main()
    #methods we can add to flask
    #if myUser != None:
        #twitter_client = TwitterClient(client).set_auth
        #checks if myUser is admin or client and sets the auth type
        #twitter_client(client).set_auth()
        #twitter_client.get_auth_url() # send to flask app
        #twitter_client.get_verifier() # get from flask app input the verifier and set it
    
    #my methods to get tweets
    #result = myClient.get_home_timeline_tweets(1)
    ##############WORKINGGGGGGGGGGGGGGGGGG
    
# STORE USER OBJECTS IN A HASHMAP
#    twitter_streamer = TwitterStreamer()
#    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)