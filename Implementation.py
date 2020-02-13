import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter
import csv
import time

dict =        { "author":[],
                "subreddit":[],
               }
# This list of terms is what is categorized as derogetory as applied to the terf subreddits(Gendercritical, terfisaslur, itsafetish)
terf_terms = ["man", "he", "him", "it", "TIF", "TIM", "TRA", "MRA", "handmaiden", "NAMALT",
              "COINing", "AGP", "autogynephilia", "transgender", "mra", "tim", "tif", "It",
              "Man", "He", "Him", "It", "agp", "Autogynephilia", "coining"]
# This list of terms is what is categorized as derogetory as applied to the incel subreddits(incelswithouthate, MensRights, MGTOW2)
incel_terms = ["wrongthink", "goolag", "chad", "meeks", "femoids", "black pill", "hypergamy", "transgender",
               "alphas", "omegas", "betas", "cucks", "stacy", "becky", "Stacy", "Becky", "Transgender",
               "Chad", "Betas", "Cucks", "Hypergamy", "Alphas", "Omegas"]

def saveSubmissions(subreddit, filename):

    sub = []
    commText = []
    commAuth = []

    for post in subreddit.top(limit=10):
        sub.append(post)

    for i in range(len(sub)):
        sub[i].comments.replace_more(limit=0)

        for comments in sub[i].comments.list():
            commText.append(comments.body)
            commAuth.append(comments.author)

        data = {'Comment Author': commAuth, 'Comment Body': commText}

    data = {'Comment Author': commAuth, 'Comment Body': commText}
    df = pd.DataFrame(data, columns = ['Comment Author', 'Comment Body'])

    df.to_csv(filename)

def save_post_author(subreddit):

    for submission in subreddit.top(limit=50):
        dict["author"].append(submission.author)
        dict['subreddit'].append(submission.subreddit)

    df = pd.DataFrame(dict)
    df.to_csv('PostAuthors.csv')

def read_csv(file):
    termcounter = 0
    totalwords = 0
    percentage = 0
    with open(file, 'r', encoding="UTF8") as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            for i in row:
                totalwords += 1
                if file == 'gendercritical.csv' or 'itsafetish.csv' or 'terfisaslur.csv':
                    if i in terf_terms:
                        termcounter += 1
                elif file == 'MGTOW2.csv' or 'MensRights.csv' or 'IncelsWithoutHate.csv':
                    if i in incel_terms:
                        termcounter += 1

    percentage = (termcounter/totalwords)
    percentage = round(percentage, 3)

    print("there are " + str(termcounter) + " derogatory terms in " + file)
    print(str(percentage) + "% of the words  in " + file + " are considered derogatory")

def main():

    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subredditList = ['gendercritical', 'MGTOW2', 'MensRights', 'itsafetish', 'terfisaslur', 'IncelsWithoutHate']
    files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv', 'IncelsWithoutHate.csv']

    #for i in subredditList:
    #subreddit = redditInstance.subreddit('MensRights')
    #    save_post_author(subreddit)
    #read_csv('gendercritical.csv')
    #saveSubmissions(subreddit, files[2])
    for i in files:
        read_csv(i)
    #saveSubmissions(subreddit, files[2])


if __name__ == '__main__':
    main()