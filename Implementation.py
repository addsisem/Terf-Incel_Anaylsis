import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter
import csv
import matplotlib.pyplot as plt

def saveSubmissions(subreddit, filename):
    """Function to grab comments from the top 24 posts of a subreddit and save them to a CSV file"""

    # Empty lists
    sub = []
    commText = []
    commAuth = []

    for post in subreddit.top(limit=24): # Loop to get top 24 posts in a subreddit
        sub.append(post)

    for i in range(len(sub)): # Ignore more comments button
        sub[i].comments.replace_more(limit=0)

        for comments in sub[i].comments.list(): # Loop to grab Comment text and author
            commText.append(comments.body)
            commAuth.append(comments.author)

    data = {'Comment Author': commAuth, 'Comment Body': commText} # Create dictionary to hold data
    df = pd.DataFrame(data, columns = ['Comment Author', 'Comment Body']) # Move data into dataframe

    df.to_csv(filename) # Save to csv file

def save_post(subreddit, filename):
    """Function to save post authors of top 1000 posts of each subreddit"""

    postAuth = []
    sub = []

    for post in subreddit.top(limit=1000): # Loop to grab top 1000 posts from a subreddit
        postAuth.append(post.author) # Store authors from the subreddit

    data = {'Post Author': postAuth}
    df = pd.DataFrame(data, columns = ['Post Author'])

    df.to_csv(filename)

def getCommentAuth(filename, filename2):

    auth = []

    df = pd.read_csv(filename)
    df.dropna(how='any', inplace=True)

    val = df.values.tolist()

    for i in range(len(val)):
        auth.append(val[i][1])

    pf = pd.DataFrame(pd.Series(auth).value_counts())

    pf.to_csv(filename2)

def comparePostAuth(filename):
    """Function to compare authors of posts in each subreddit to determine user frequency"""

    auth = []

    df = pd.read_csv(filename)
    df.dropna(how='any', inplace=True)

    val = df.values.tolist()

    for i in range(len(val)):
        auth.append(val[i][1])

    pf = pd.DataFrame(pd.Series(auth).value_counts())

    pf.to_csv(filename)

def compareCSVAuth(filename, filename2):
    """Function to compare Post Authors across CSV files"""

    auth = []
    authors = []
    cross = []

    df = pd.read_csv(filename)
    pf = pd.read_csv(filename2)

    val = df.values.tolist()
    lav = pf.values.tolist()

    for i in range(len(val)):
        auth.append(val[i][0])

    for j in range(len(lav)):
        authors.append(lav[j][0])

    for i in auth:
        count = 0
        for j in authors:
            if i == j:
                count = count + 1
        if count == 1:
            cross.append(i)

    print()
    print("Users Who Crossposted in ", filename, " and ", filename2)

    for i in range(len(cross)):
        print(cross[i])

def read_csv():

    # This list of terms is what is categorized as derogetory as applied to the terf subreddits(Gendercritical, terfisaslur, itsafetish)
    terf_terms = ["man", "he", "him", "it", "TIF", "TIM", "TRA", "MRA", "handmaiden", "NAMALT",
                  "COINing", "AGP", "autogynephilia", "transgender", "mra", "tim", "tif", "It",
                  "Man", "He", "Him", "It", "agp", "Autogynephilia", "coining"]
    # This list of terms is what is categorized as derogatory as applied to the incel subreddits(incelswithouthate, MensRights, MGTOW2)
    incel_terms = ["wrongthink","chad", "meeks", "femoids", "hypergamy", "transtrender",
                   "alphas", "omegas", "betas", "cucks", "cuck", "Cuck", "stacy", "becky", "Stacy", "Becky", "Transtrender",
                   "Chad", "Betas", "Cucks", "Hypergamy", "Alphas", "Omegas"]

    files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv',
             'IncelsWithoutHate.csv']

    sub = []
    percentages = []
    total = []


    for h in files:
        termcounter = 0
        totalwords = 0
        percentage = 0
        with open(h, 'r', encoding="UTF8") as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                for i in row:
                    totalwords += 1
                    if h == 'gendercritical.csv' or 'itsafetish.csv' or 'terfisaslur.csv':
                        if i in terf_terms:
                            termcounter += 1
                    elif h == 'MGTOW2.csv' or 'MensRights.csv' or 'IncelsWithoutHate.csv':
                        if i in incel_terms:
                            termcounter += 1
        percentage = (termcounter / totalwords)
        percentage = round(percentage, 3)

        sub.append(h)
        percentages.append(percentage)
        total.append(termcounter)

        print("there are " + str(termcounter) + " derogatory terms in " + h)
        print(str(percentage) + "% of the words  in " + h + " are considered derogatory")



    data = {'Subreddit': sub, 'Percentage': percentages, 'Total # of terms': total}  # Create dictionary to hold data
    df = pd.DataFrame(data, columns=['Subreddit', 'Percentage', 'Total # of terms'])  # Move data into dataframe

    df.to_csv("Percentage.csv")

def Show_results(filename):

    df = pd.read_csv(filename)
    plt.figure(0)  # Fourth Figure
    plt.rc('xtick', labelsize=6)
    plt.xlabel("Subreddit")
    plt.ylabel("Percentage of Derogatory terms used")
    plt.title("Percentage of Derogatory terms used per subreddit")
    # Code for Bar Graph here
    plt.bar(df['Subreddit'], df['Percentage'])

    plt.figure(1)
    plt.rc('xtick', labelsize=6)
    plt.xlabel("Subreddit")
    plt.ylabel("Total # of Derogatory terms used")
    plt.title("Total # of Derogatory terms used per subreddit")
    plt.bar(df['Subreddit'], df['Total # of terms'])

    plt.show()


def main():

    # Create a redditInstance with praw for parsing
    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subredditList = ['gendercritical', 'MGTOW2', 'MensRights', 'itsafetish', 'terfisaslur', 'IncelsWithoutHate']
    files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv', 'IncelsWithoutHate.csv']
    authFiles = ['gendercriticalAuth.csv', 'MGTOW2Auth.csv', 'MensRightsAuth.csv', 'itsafetishAuth.csv', 'terfisaslurAuth.csv', 'IncelsWithoutHateAuth.csv']
    authCommFiles = ['gendercriticalCommAuth.csv', 'MGTOW2CommAuth.csv', 'MensRightsCommAuth.csv', 'itsafetishCommAuth.csv',
                 'terfisaslurCommAuth.csv', 'IncelsWithoutHateCommAuth.csv']

    #for k in range(len(subredditList)): # Loop to loop through the saveSubmissions function
     #   subreddit = redditInstance.subreddit(subredditList[k])
      #  save_post(subreddit, authFiles[k])
      #  saveSubmissions(subreddit, files[k])
      #compareAuth(authFiles[k])
      #  getCommentAuth(files[k], authCommFiles[k])

    #read_csv('gendercritical.csv')
    #saveSubmissions(subreddit, files[2])

    #compareCSVAuth(authCommFiles[0], authCommFiles[3])

    #for i in files:
    #read_csv()
    Show_results('Percentage.csv')
    #saveSubmissions(subreddit, files[2])



if __name__ == '__main__':
    main()