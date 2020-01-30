import praw

# Get attributes of submission object
#attributes = next(submission).__dict__.keys()

# Get next submission object from listing generator
#first_post = next(submission)


class Reddit:

    def __init__(self, credentials):
        self.reddit = None
        self.submission = None

        with open(credentials, 'r') as infile:
            creds = infile.read().splitlines()

        self.reddit = praw.Reddit(client_id=creds[0], client_secret=creds[1],
                                    password=creds[3], user_agent='scrapeSpike by bestaccountantevar',
                                    username=creds[2])

    def get_submissions(self, subreddit):
        self.submission = self.reddit.subreddit(subreddit).hot(limit=5)

    def get_post_details(self, *args):
        urls = []
        for i in self.submission:
            for j in args:
                #print(getattr(i, j))
                urls.append(getattr(i, j))

        return urls

my_reddit = Reddit('credentials.txt')
my_reddit.get_submissions('askreddit')
my_reddit.get_post_details('url', 'thumbnail')
