import praw
import consts


# Get attributes of submission object
# attributes = next(submission).__dict__.keys()

# Get next submission object from listing generator
# first_post = next(submission)


class Reddit:
    __instance = None

    @staticmethod
    def get_instance():
        if Reddit.__instance == None:
            Reddit()
        return Reddit.__instance

    def __init__(self):
        self.reddit = None
        self.submission = None
        self.credentials = 'credentials.txt'

        if Reddit.__instance != None:
            raise Exception("Error: class is a singleton and object %s exists" % Reddit.__instance)
        else:
            Reddit.__instance = self

        with open(self.credentials, 'r') as infile:
            creds = infile.read().splitlines()

        self.reddit = praw.Reddit(client_id=creds[0], client_secret=creds[1],
                                  password=creds[3], user_agent='scrapeSpike by bestaccountantevar',
                                  username=creds[2])

    def get_submissions(self, subreddit):
        self.submission = self.reddit.subreddit(subreddit).hot(limit=consts.NUM_SUBS)

    def get_post_details(self, *args):
        urls = []
        for i in self.submission:
            for j in args:
                # print(getattr(i, j))
                urls.append(getattr(i, j))

        # print(urls)
        return urls

class Subreddits:   #TODO: I doubt this will work but this is the idea. Initialize a Subreddits PRAWModel instance. Ref: https://praw.readthedocs.io/en/latest/code_overview/reddit/subreddits.html
    __instance = None
    
    @staticmethod
    def get_instance():
        if Subreddits.__instance == None:
            Subreddits(Reddit)
        return Subreddits.__instance
    
    def __init__(self):
        if Subreddits.__instance != None:
            raise Exception("Error: class is a singleton and object %s exists" % Reddit.__instance)
        else:
            Subreddits.__instance = self


# my_reddit = Reddit('credentials.txt')
# my_reddit.get_submissions('dogswithjobs')
# my_reddit.get_post_details('url', 'thumbnail')
