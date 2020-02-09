import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter

def saveSubmissions(subreddit, filename):

    sub = []
    postAuth = []
    commText = []
    commAuth = []

    for post in subreddit.top(limit=1):
        sub.append(post)

    for i in range(len(sub)):
        postAuth.append(sub[i].author)
        sub[i].comments.replace_more(limit=0)

        for comments in sub[i].comments.list():
            commText.append(comments.body)
            commAuth.append(comments.author)

    df = pd.DataFrame(columns = ['Post Author', 'Comment Author', 'Comment Body'])

    for i in range(len(sub)):
        df.loc[i, 'Post Author'] = postAuth[i]
        for j in range(len(commText)):
            df.loc[j, 'Comment Body'] = commText[j]
            df.loc[j, 'Comment Author'] = commAuth[j]

    df.to_csv(filename)


def main():

    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subredditList = ['gendercritical', 'MGTOW2', 'MensRights', 'itsafetish', 'terfisaslur', 'incelswithouthate']
    files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv', 'incelswithouthate.csv']

    #for i in range(len(subredditList)):
    subreddit = redditInstance.subreddit(subredditList[0])
    saveSubmissions(subreddit, files[0])


if __name__ == '__main__':
    main()