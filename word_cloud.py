import nltk
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split

import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS


def generate_wordcloud(data, color='black'):
    """
    This method generates the wordcloud for the given data
    """
    words = ' '.join(data)
    filtered_word = " ".join([word for word in words.split()
                             if 'http' not in word
                             and not word.startswith('@')
                             and not word.startswith('#')
                             and word != 'RT'
                             ])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color=color,
                          width=2500,
                          height=2000
                          ).generate(filtered_word)

    plt.figure(1, figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')

    plt.savefig('output/train_ds_wc.png')


def get_words_in_tweets(tweets):
    """
    This method generates the overall words list
    """
    all = []
    for (words, sentiment) in tweets:
        all.extend(words)
    return all


def get_word_features(wordlist):
    """
    This method calculates the word frequency in the given words list.
    """
    wordlist = nltk.FreqDist(wordlist)
    features = wordlist.keys()
    return features


if __name__ == '__main__':
    u_tweets = []
    stopwords_set = set(stopwords.words("english"))

    ds = pd.read_csv('input/sentiment.csv')
    train, test = train_test_split(ds, test_size=0.1)

    train = train[train.sentiment != "Neutral"]

    train_pos = train[train['sentiment'] == 'Positive']
    train_pos = train_pos['text']
    train_neg = train[train['sentiment'] == 'Negative']
    train_neg = train_neg['text']

    for index, row in train.iterrows():
        words_filtered = [e.lower() for e in row.text.split() if len(e) >= 3]
        words_cleaned = [word for word in words_filtered
                         if 'http' not in word
                         and not word.startswith('@')
                         and not word.startswith('#')
                         and word != 'RT']
        words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
        u_tweets.append((words_without_stopwords, row.sentiment))

    w_features = get_word_features(get_words_in_tweets(u_tweets))

    generate_wordcloud(w_features, color='#FFFAF0')

