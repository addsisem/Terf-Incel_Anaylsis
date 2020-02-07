import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter

def saveSubmissions(subreddit):

    sub = []
    title = []

    for post in subreddit.top(limit=50):
        sub.append(post.subreddit)
        title.append(post.title)

    df = pd.DataFrame(columns = ['Subreddit', 'Top'])

    for i in range(len(sub)):
        df.loc[i, 'Subreddit'] = sub[i]
        df.loc[i, 'Top'] = title[i]

    df.to_csv('A5.csv') #FIX

def main():

    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subreddit = redditInstance.subreddit('gendercritical')
    subreddit1 = redditInstance.subreddit('MGTOW2')
    subreddit2 = redditInstance.subreddit('MensRights')
    subreddit3 = redditInstance.subreddit('itsafetish')
    subreddit4 = redditInstance.subreddit('terfisaslur')
    subreddit5 = redditInstance.subreddit('incelswithouthate')

    saveSubmissions(subreddit)
    saveSubmissions(subreddit1)
    saveSubmissions(subreddit2)
    saveSubmissions(subreddit3)
    saveSubmissions(subreddit4)
    saveSubmissions(subreddit5)

if __name__ == '__main__':
    main()