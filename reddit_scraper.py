import praw


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
        try:
            self.submission = self.reddit.subreddit(subreddit).hot(limit=5)
        except Exception as e:
            self.logfile.write('Get submission error: %s' % e)

    def get_post_details(self, *args):
        urls = []
        for i in self.submission:
            for j in args:
                urls.append(getattr(i, j))

        return urls
