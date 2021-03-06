import nltk
import praw
import pandas as pd
import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import gensim
import re
import random
from nltk import classify
from nltk import NaiveBayesClassifier
from gensim import corpora
from gensim import models
from pprint import pprint
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk import word_tokenize, re
from nltk.util import ngrams
import codecs
import string
from textblob import TextBlob
from praw import Reddit
from smart_open import smart_open
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.collocations import *
import os

def saveSubmissions(subreddit, filename):
    """Function to grab comments from the top 24 posts of a subreddit and save them to a CSV file"""

    # Empty lists
    sub = []
    commText = []
    commAuth = []

    for post in subreddit.top(limit=50): # Loop to get top 24 posts in a subreddit
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

def Remove_Stopwords(filename):

    df = pd.read_csv(filename)
    df.drop(df.columns[[0, 1]], axis=1, inplace=True) #Remove comment author
    df.dropna(how='any', inplace=True)
    df.to_csv(filename)

    newfile = filename.replace('.csv', '.txt')
    file = codecs.open(newfile, 'w', encoding="UTF8")

    if filename == 'gendercritical.csv' or 'itsafetish.csv' or 'terfisaslur.csv' or 'GenderCriticalGuys.csv' or 'GenderCynicalCritical.csv' or 'TrollGC.csv':

        terf_terms = ["man", "he", "him", "it", "TIF", "TIM", "TRA", "MRA", "handmaiden", "NAMALT",
                      "COINing", "AGP", "autogynephilia", "transgender", "mra", "tim", "tif", "It",
                      "Man", "He", "Him", "It", "agp", "Autogynephilia", "coining"]

        stop_words = (stopwords.words('english'))
        final_stop_words = set([word for word in stop_words if word not in terf_terms])

        with open(filename, 'r', encoding="UTF8") as csvfile:  # Actually opens the files for reading
            reader = csv.reader(csvfile, delimiter=',', quotechar='|') # Separates file by commas
            for line in reader:  # Looks at each separated value
                for row in line:  # Looks at each line
                    sentence = re.split(' ', row) # Seperates words from lines using spaces as delimiters
                    for i in sentence: # Loops through each word
                        if i.lower() not in final_stop_words and i.isdigit() is False:
                            file.write(i)
                            file.write(' ')
                            print(i)
        file.close()

    elif filename == 'MGTOW2.csv' or 'MensRights.csv' or 'IncelsWithoutHate.csv' or 'trufemcels.csv' or 'KotakuInAction.csv' or 'MensRants.csv':

        newfile = filename.replace('.csv', '.txt')
        file = codecs.open(newfile, 'w', encoding="UTF8")
        stop_words = (stopwords.words('english'))

        with open(filename, 'r', encoding="UTF8") as csvfile:  # Actually opens the files for reading
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for line in reader:  # Looks at each separated value
                for row in line:  # Looks at each line
                    sentence = re.split(' ', row) # Seperates words from lines using spaces as delimiters
                    for i in sentence: # Loops through each word
                        if i.lower() not in stop_words and i.isdigit() is False:
                            file.write(i)  # This line causes errors
                            file.write(' ')
                            print(i)
        file.close()


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

    df2 = pd.read_csv(filename)
    pf2 = df2.head(15)

    pf2.to_csv(filename)

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

def read_csv(filename, subreddit):
    """
    This function reads each csv we have, compares each word to a special dictionary
    that is determined based on file name. Retrieves the total number of derogatory terms
    used in each csv and creates a percentage from it
    :return:
    """

    # This list of terms is what is categorized as derogetory as applied to the terf subreddits(Gendercritical, terfisaslur, itsafetish)
    terf_terms = ["man", "he", "him", "it", "TIF", "TIM", "TRA", "MRA", "handmaiden", "NAMALT",
                  "COINing", "AGP", "autogynephilia", "transgender", "mra", "tim", "tif", "It",
                  "Man", "He", "Him", "It", "agp", "Autogynephilia", "coining"]
    # This list of terms is what is categorized as derogatory as applied to the incel subreddits(incelswithouthate, MensRights, MGTOW2)
    incel_terms = ["wrongthink", "chad", "meeks", "femoids", "hypergamy", "transtrender",
                   "alphas", "omegas", "betas", "cucks", "stacy", "becky", "Stacy", "Becky", "Transtrender",
                   "Chad", "Betas", "Cucks", "Hypergamy", "Alphas", "Omegas"]

    #files = ['gendercritical.csv', 'MGTOW2.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv',
     #        'IncelsWithoutHate.csv']

    # Lists that will be used to create a csv
    sub = []
    percentages = []
    total = []

    termcounter = 0
    totalwords = 0

    with open(filename, 'r', encoding="UTF8") as csvfile: # Actually opens the files for reading
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader: # Looks at each line
            for i in row: # Looks at each word
                totalwords += 1
                if filename == 'gendercritical.csv' or 'itsafetish.csv' or 'terfisaslur.csv' or 'GenderCriticalGuys.csv'or 'GenderCynicalCritical.csv' or 'TrollGC.csv':
                    # Depending on the csv, a specific dictionary will be used for comparison
                    if i in terf_terms:
                        termcounter += 1
                elif filename == 'MGTOW2.csv' or 'MensRights.csv' or 'IncelsWithoutHate.csv' or 'trufemcels.csv' or 'KotakuInAction.csv' or 'MensRants.csv':
                    if i in incel_terms:
                        termcounter += 1

    percentage = (termcounter / totalwords) # Basic math to calculate a percentage
    percentage = round(percentage, 3) # Round the percentage to make it pretty

    sub.append(subreddit) # append the filename to a list
    percentages.append(percentage) # append the percentage to a list
    total.append(termcounter) # append the total number of derogatory terms used in the csv to a list

    # Print the results in a readable format
    print("there are " + str(termcounter) + " derogatory terms in " + filename)
    print(str(percentage) + "% of the words  in " + filename + " are considered derogatory")

    # Create the Dataframe and send it to the new csv
    data = {'Subreddit': sub, 'Percentage': percentages, 'Total # of terms': total}  # Create dictionary to hold data
    df = pd.DataFrame(data, columns=['Subreddit', 'Percentage', 'Total # of terms'])  # Move data into dataframe

    # https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
    df.to_csv("Percentage.csv", mode='a', header=False) # Credit to root and tlingf from Stack Overflow

def authPosts(redditInstance, authfile):
    """This function will loop through the top users of each subreddit and grab the user's top submissions (or posts)
    across Reddit"""

    auth = []

    df = pd.read_csv(authfile)

    val = df.values.tolist()

    for i in range(len(val)):
        auth.append(val[i][1])

    temp = []

    for user in auth:
        temp.clear()
        print("User: ", user)
        for submission in redditInstance.redditor(user).submissions.top('all'):
            temp.append(submission.subreddit)
        print(Counter(temp))

def Show_results(filename, authfile):
    """
    This function uses a csv file to create several bar graphs that communicate our findings
    :param filename:
    :return:
    """

    df = pd.read_csv(filename) # Reads the given csv file so a graph can be made from the data
    plt.figure(0)  # Fourth Figure
    plt.rc('xtick', labelsize=7) # Sets the font size of the Xlabel
    plt.xlabel("Subreddit") # Label the X axis
    plt.ylabel("Percentage of Derogatory terms used") # Label the Y axis
    plt.title("Percentage of Derogatory terms used per subreddit") # Sets the title for graph
    plt.bar(df['Subreddit'], df['Percentage']) # uses the read file and the first two columns of data

    plt.figure(1) # Creates a second graph
    plt.rc('xtick', labelsize=7)
    plt.xlabel("Subreddit")
    plt.ylabel("Total # of Derogatory terms used")
    plt.title("Total # of Derogatory terms used per subreddit")
    plt.bar(df['Subreddit'], df['Total # of terms']) # This line creates a bar graph

    plt.figure(2)
    pf = pd.read_csv(authfile) # need to condense auth data

    list = pf.values.tolist()

    x = []
    y = []

    for i in range(len(list)):
        x.append(list[i][2])
        y.append(list[i][1])

    plt.scatter(x, y)

    plt.xlabel("# of Posts")  # Label the Y axis
    plt.ylabel("User")  # Label the X axis
    plt.title("# of Posts per User")  # Set the plot’s title

    plt.show()

def topicModel(filename):

    # Create gensim dictionary from a single CSV file
    dictionary = corpora.Dictionary(simple_preprocess(line, deacc=True) for line in
                                    open(filename,
                                         encoding='utf-8'))
    corpus = [dictionary.doc2bow(simple_preprocess(line)) for line in open(filename,
                                         encoding='utf-8')]

    tfidf = models.TfidfModel(corpus, smartirs='ntc') # This model adds weights to each unique word in the corpus
    for doc in tfidf[corpus]: # applies weight to each line
        print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc]) # print the tfidf matrix out

    # Token to Id map
    #pprint(dictionary.token2id)

def Bigrams(filename):
    """
    This function creates bigrams using two different methods from a given dataset.
    :param filename:
    :return:
    """

    file = codecs.open(filename, 'r', encoding="UTF8")

    for line in file:
        token = nltk.word_tokenize(line)
        bigram = list(ngrams(token, 2))

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(bigram)
    print(finder.nbest(bigram_measures.pmi, 10))

    # Construct bigram
    print(bigram) # comment out this line to use other method

def Trigrams(filename):
    """
    This function creates trigrams using two different methods from a given dataset.
    :param filename:
    :return:
    """

    file = codecs.open(filename, 'r', encoding="UTF8")

    for line in file:
        token = nltk.word_tokenize(line)
        trigram = list(ngrams(token, 3))

    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(trigram)
    print(finder.nbest(trigram_measures.pmi, 10))

    # Construct trigram
    print(trigram) # comment out this line to use other method

def remove_noise(tweet_tokens, stop_words = ()):
    """
    Function taken from https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
    to be used in the sentiment analysis function
    :param tweet_tokens:
    :param stop_words:
    :return:
    """

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def SentimentAnalysis(filename):
    """
    file = codecs.open(filename, 'r', encoding="UTF8")
    negative = 0
    positive = 0
    neutral = 0
    totallines = 0
    for line in file:
        totallines = totallines + 1
        analysis = TextBlob(line)
        print(line)
        if analysis.sentiment.polarity > 0:
            positive = positive + 1
        elif analysis.sentiment.polarity == 0:
            neutral = neutral + 1
        else:
            negative = negative + 1

    positive_lines = (positive/totallines)
    positive_lines = round(positive_lines, 3)
    negative_lines = (negative/totallines)
    negative_lines = round(negative_lines, 3)
    neutral_lines = (neutral/totallines)
    neutral_lines = round(neutral_lines, 3)

    print(str(positive_lines) + "% of the lines in " + filename + " are considered positive.")
    print(str(neutral_lines) + "% of the lines in " + filename + " are considered neutral.")
    print(str(negative_lines) + "% of the lines in " + filename + " are considered negative.")
    """
    stop_words = (stopwords.words('english'))
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    file = codecs.open(filename, 'r', encoding="UTF8")

    for line in file:
        token = nltk.word_tokenize(line)
        print(token, classifier.classify(dict([token, True] for token in token)))


def get_tweets_for_model(cleaned_tokens_list):
    """Taken from https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
    to be used in sentiment analysis"""
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def main():

    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    # Credit to Tad from Stack Overflow
    csv.field_size_limit(100000000) # Extends max field size for a csv so no errors are thrown.

    # Create a redditInstance with praw for parsing
    redditInstance = praw.Reddit(user_agent='A5', client_id='c9MX-PNSpd4Tjw',
                                 client_secret="kI-F1f7g1-cWqujoQYIgwaG6-QE",
                                 username='sisemorea', password='khg=QrekT78335T')

    subredditList = ['gendercritical', 'MensRights', 'itsafetish', 'terfisaslur', 'IncelsWithoutHate',
                     'MensRants',
                    'GenderCynicalCritical', 'TrollGC', 'GenderCriticalGuys', 'trufemcels', 'KotakuInAction', 'MGTOW2']
    files = ['gendercritical.csv', 'MensRights.csv', 'itsafetish.csv', 'terfisaslur.csv', 'IncelsWithoutHate.csv',
             'MensRants.csv', 'GenderCynicalCritical.csv', 'TrollGC.csv', 'GenderCriticalGuys.csv', 'trufemcels.csv', 'KotakuInAction.csv', 'MGTOW2.csv']
    authFiles = ['gendercriticalAuth.csv', 'MensRightsAuth.csv', 'itsafetishAuth.csv', 'terfisaslurAuth.csv', 'IncelsWithoutHateAuth.csv', 'MensRantsAuth.csv',
                 'GenderCynicalCriticalAuth.csv', 'TrollGCAuth.csv', 'GenderCriticalGuysAuth.csv', 'trufemcelsAuth.csv', 'KotakuInActionAuth.csv', 'MGTOW2Auth.csv']
    authCommFiles = ['gendercriticalCommAuth.csv', 'MensRightsCommAuth.csv', 'itsafetishCommAuth.csv',
                 'terfisaslurCommAuth.csv', 'IncelsWithoutHateCommAuth.csv', 'MensRantsCommAuth.csv', 'GenderCynicalCriticalCommAuth.csv', 'TrollGCCommAuth.csv',
                     'GenderCriticalGuysCommAuth.csv', 'trufemcelsCommAuth.csv', 'KotakuInActionCommAuth.csv', 'MGTOW2CommAuth.csv']

    #for k in range(len(subredditList)): # Loop to loop through the saveSubmissions function
        #subreddit = redditInstance.subreddit(subredditList[k])
        #save_post(subreddit, authFiles[k])
        #saveSubmissions(subreddit, files[k])
        #getCommentAuth(files[k], authCommFiles[k])
        #read_csv(files[k], subredditList[k])
        #comparePostAuth(authFiles[k])

    #compareCSVAuth(authCommFiles[0], authCommFiles[3])
    #Show_results('Percentage.csv', 'terfisaslurAuth.csv')
    #topicModel('MensRights.txt')
    #Bigrams('gendercritical.txt')
    #Trigrams('gendercritical.txt')
    #Remove_Stopwords('gendercritical.csv')
    #Bigrams('gendercritical.txt')
    #Remove_Stopwords(files[k])
    # topicModel('gendercritical.txt')
    #authPosts(redditInstance, 'gendercriticalAuth.csv')
    SentimentAnalysis('gendercritical.csv')


if __name__ == '__main__':
    main()