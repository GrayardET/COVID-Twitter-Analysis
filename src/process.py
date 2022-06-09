import pandas as pd
import re
import nltk
from nltk.corpus import wordnet

def main():
    # read in data
    df = pd.read_csv('covid.csv')
    stopwords = load_stop_words()

    # tokenize and post process, remove unnecessary words appearing in tweets(like urls and usernames)
    tweet_words = []
    str_lis = []
    for t in df['text']:
        t = t.lower()
        tokens = tokenize(t)
        tmp = []
        for token in tokens:
            if token in stopwords:
                continue
            if not wordnet.synsets(token):
                continue
            # repalce usernames with @USER
            user = re.sub(r'@[\w\W]+', '@USER', token)
            # replace with URL
            url = re.sub(r'https[\w\W]+','URL',user)
            if url in stopwords:
                continue
            tmp.append(url)
        tweet_words.append(tmp)
        st = ' '.join([str(item) for item in tmp])
        str_lis.append(st)
    df['tweet_words'] = tweet_words
    df['tweets'] = str_lis

    # remove duplicates
    df.drop_duplicates(subset=['tweets'], inplace=True)

    df.drop(columns='tweet_words', inplace=True)
    print(len(df))
    df.to_csv("../data/covid.csv", index=False)


def tokenize(text):
    words = []
    # print(text.split())
    for token in text.split():
        # find wouldn't kind word
        words.extend(re.findall(r"\w+-\w+|https.+|\.+|\d+[\.,]\d+|[@#]\w+|[+-]\d+|(?:(?!n[’'])\w)+|\w?[’']\w+|[^\s\w]", token))
        # words.extend(re.findall(r"(?:(?!.')\w)+|\w?'\w+|[^\s\w]", token))
    return words


def load_stop_words():
    stop_words = set()
    words = open("../data/stopwords.txt", "r").read().split("\n")
    for word in words:
        stop_words.add(word.strip())
    return stop_words


if __name__ == '__main__':
    main()
