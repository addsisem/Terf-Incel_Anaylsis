import praw
from praw.models import MoreComments
import pandas as pd
import csv

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

    data = {'Post Author': postAuth} # Format data
    df = pd.DataFrame(data, columns = ['Post Author']) # Create a dataframe with column formatting

    df.to_csv(filename) # Export to csv

def getCommentAuth(filename, filename2):
    """Function to seperate comment authors from previous csv file into a new csv file"""

    auth = []

    df = pd.read_csv(filename) # Read csv file
    df.dropna(how='any', inplace=True) # Removes any deleted users within initial author list

    val = df.values.tolist()

    for i in range(len(val)):
        auth.append(val[i][1])

    pf = pd.DataFrame(pd.Series(auth).value_counts()) # Counter using the pandas library

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

    val = df.values.tolist() # Convert dataframe into a list
    lav = pf.values.tolist()

    for i in range(len(val)):
        auth.append(val[i][0]) # Position of authors name in list

    for j in range(len(lav)):
        authors.append(lav[j][0])

    for i in auth:
        count = 0
        for j in authors:
            if i == j: # Compare author's names
                count = count + 1
        if count == 1: # If the author is present in both subreddits
            cross.append(i) # Add author to list

    print() # Output formatting
    print("Users Who Crossposted in ", filename, " and ", filename2)

    for i in range(len(cross)):
        print(cross[i])

def read_csv(file):
    """Function to check frequency of derogatory terms used in each subreddit"""

    # This list of terms is what is categorized as derogetory as applied to the terf subreddits(Gendercritical, terfisaslur, itsafetish)
    terf_terms = ["man", "he", "him", "it", "TIF", "TIM", "TRA", "MRA", "handmaiden", "NAMALT",
                  "COINing", "AGP", "autogynephilia", "transgender", "mra", "tim", "tif", "It",
                  "Man", "He", "Him", "It", "agp", "Autogynephilia", "coining"]
    # This list of terms is what is categorized as derogatory as applied to the incel subreddits(incelswithouthate, MensRights, MGTOW2)
    incel_terms = ["wrongthink", "chad", "meeks", "femoids", "hypergamy", "transtrender",
                   "alphas", "omegas", "betas", "cucks", "stacy", "becky", "Stacy", "Becky", "Transtrender",
                   "Chad", "Betas", "Cucks", "Hypergamy", "Alphas", "Omegas"]

    termcounter = 0
    totalwords = 0
    percentage = 0

    with open(file, 'r', encoding="UTF8") as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            for i in row:
                totalwords += 1 # Counter for derogatory terms
                if file == 'gendercritical.csv' or 'itsafetish.csv' or 'terfisaslur.csv': # Checking similar ("TERF") subreddits
                    if i in terf_terms:
                        termcounter += 1
                elif file == 'MGTOW2.csv' or 'MensRights.csv' or 'IncelsWithoutHate.csv': # Checking similar ("Incel") subreddits
                    if i in incel_terms:
                        termcounter += 1

    # Getting total percentages for cleaner data output
    percentage = (termcounter/totalwords)
    percentage = round(percentage, 3)

    print("there are " + str(termcounter) + " derogatory terms in " + file)
    print(str(percentage) + "% of the words  in " + file + " are considered derogatory")

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

    compareCSVAuth(authCommFiles[0], authCommFiles[3])

    #for i in files:
     #   read_csv(i)
    #saveSubmissions(subreddit, files[2])



if __name__ == '__main__':
    main()