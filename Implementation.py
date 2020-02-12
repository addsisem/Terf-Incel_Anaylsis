import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter
import csv

dict =        { "author":[],
                "subreddit":[],
               }
# This list of terms is what is categorized as derogetory as applied to the terf subreddits(Gendercritical, terfisaslur, itsafetish)
terf_terms = ["man", "he", "him", "it", "TIF", "TIM", "TRA", "MRA", "handmaiden", "NAMALT",
              "COINing", "AGP", "autogynephilia", "transgender"]
# This list of terms is what is categorized as derogetory as applied to the incel subreddits(incelswithouthate, MensRights, MGTOW2)
incel_terms = ["wrongthink", "goolag", "chad", "meeks", "femoids", "black pill", "hypergamy", "transgender",
               "alphas", "omegas", "betas", "cucks", "stacy", "becky", "Stacy", "Becky"]

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

def read_csv(file):
    termcounter = 0
    with open(file, 'r', encoding="UTF8") as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            for i in row:
                if file == 'gendercritical.csv' or 'itsafetish.csv' or 'terfisaslur.csv':
                    if i in terf_terms:
                        termcounter += 1
                elif file == 'MGTOW2.csv' or 'MensRights.csv' or 'IncelsWithoutHate.csv':
                    if i in incel_terms:
                        termcounter += 1

    print(termcounter)

def main():

    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subredditList = ['gendercritical', 'MGTOW2', 'MensRights', 'itsafetish', 'terfisaslur', 'IncelsWithoutHate']
    files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv', 'IncelsWithoutHate.csv']

    #for i in subredditList:
    #    subreddit = redditInstance.subreddit(i)
    #    save_post_author(subreddit)
    read_csv('gendercritical.csv')
    #saveSubmissions(subreddit, files[2])


if __name__ == '__main__':
    main()