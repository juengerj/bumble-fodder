import praw


class Reddit:

    def __init__(self, credentials):
        self.reddit = None
        self.submission = None
        self.logfile = None

        with open('log.txt', 'a') as logfile:
            self.logfile = logfile

        with open(credentials, 'r') as infile:
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
