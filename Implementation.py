import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter

dict =        { "author":[],
                "subreddit":[],
               }

def saveSubmissions(subreddit, filename):

    sub = []
    postAuth = []
    commText = []
    commAuth = []

    for post in subreddit.top(limit=10):
        sub.append(post)

    for i in range(len(sub)):
        sub[i].comments.replace_more(limit=0)

        for comments in sub[i].comments.list():
            commText.append(comments.body)
            commAuth.append(comments.author)

    df = pd.DataFrame(columns = ['Comment Author', 'Comment Body'])

    for j in range(len(commText)):
        df.loc[j, 'Comment Body'] = commText[j]
        df.loc[j, 'Comment Author'] = commAuth[j]

    df.to_csv(filename)

def save_post_author(subreddit):
    for submission in subreddit.top(limit=50):
        dict["author"].append(submission.author)
        dict['subreddit'].append(submission.subreddit)
    df = pd.DataFrame(dict)
    df.to_csv('PostAuthors.csv')

#def read_csv(files):
#    for i in range(files):
#        for word in i:
#            if word in

def main():

    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subredditList = ['gendercritical', 'MGTOW2', 'MensRights', 'itsafetish', 'terfisaslur', 'IncelsWithoutHate']
    files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv', 'IncelsWithoutHate.csv']

    for i in subredditList:
        subreddit = redditInstance.subreddit(i)
        save_post_author(subreddit)

    #saveSubmissions(subreddit, files[2])


if __name__ == '__main__':
    main()