import json
import math
import pandas as pd
from itertools import islice
import pprint
pp = pprint.PrettyPrinter()
import nltk
from nltk.stem import WordNetLemmatizer

def main():
    df = pd.read_csv('../data/covid_to_compute3.csv', dtype= str)
    df = df.dropna()
    print(len(df))
    # second time processing: lemmatizaton
    lemmatizer = WordNetLemmatizer()
    for i,row in df.iterrows():
        temp_sent = []
        sent = row.tweets
        # print(sent)

        for word in sent.split(' '):
            # print(word)
            if word == 'doses':
               lem_word = lemmatizer.lemmatize(word, 'v')
            else: 
                lem_word = lemmatizer.lemmatize(word)
            # print(lem_word)
            temp_sent.append(lem_word)
        
        # print(temp_sent)
        df.at[i, 'tweets'] = ' '.join(temp_sent)

    for i, idx in df.iterrows():
        
        if idx.Topic == 's' or idx.Topic == 't':
            df.at[i, 'Topic'] = 'l'

    policy = df[df['Topic'] == 'p']
    vaccine = df[df['Topic'] == 'v']
    health = df[df['Topic'] == 'h']
    life = df[df['Topic'] == 'l']
    covid = df[df['Topic'] == 'c']
    other = df[df['Topic'] == 'o']

    # build total word counts dictionary
    total_words = dict()
    topics = [policy, vaccine, health, life, covid, other]
    for t in topics:
        count_words(t, total_words)

    tmp = dict()
    for idx, w in enumerate(sorted(total_words, key=total_words.get, reverse=True)):
        tmp[w] = total_words[w]
    # print(len(tmp))

    # count = 0
    # for el in tmp:
    #     if(count >= 20):
    #         break
    #     else:
    #         print(f'current word is {el}, count is {tmp[el]}')


    # count for each topic (tf values)
    policy_ct = dict()
    count_words(policy, policy_ct)

    vaccine_ct = dict()
    count_words(vaccine, vaccine_ct)

    health_ct = dict()
    count_words(health, health_ct)

    life_ct = dict()
    count_words(life, life_ct)

    covid_ct = dict()
    count_words(covid, covid_ct)

    other_ct = dict()
    count_words(other, other_ct)

    # compute tfidf values for each word
    topics = [policy_ct, vaccine_ct, health_ct, life_ct, covid_ct, other_ct]
    topic_names = ['policy', 'vaccine', 'health', 'life', 'covid', 'other']

    topics_top_count = {}
    for i,topic in enumerate(topics):
        sorted_topic_count = {k: v for k, v in sorted(topic.items(), key=lambda term: term[1], reverse=True)}
        topics_top_count[topic_names[i]] = sorted_topic_count

    for key, value in topics_top_count.items():
        if "vaccine" in value.keys():
            print(f"vaccine in dictionary {key}: {value['vaccine']}")
        else:
            print(f"vaccine in dictionary {key}: 0")
    # print(topics_top_count['covid']['infect'])
    # print(topics_top_count['covid']["adding"])
    # word_frequency_count = json.dumps(topics_top_count, indent=2)
    
    # print(word_frequency_count)
        
    outdict = {
        'policy': list(list(x) for x in tfidf(policy_ct, topics).items()),
        'vaccine': list(list(x) for x in tfidf(vaccine_ct, topics).items()),
        'health': list(list(x) for x in tfidf(health_ct, topics).items()),
        'life': list(list(x) for x in tfidf(life_ct, topics).items()),
        'covid': list(list(x) for x in tfidf(covid_ct, topics).items()),
        'other': list(list(x) for x in tfidf(other_ct, topics).items())
    }

    ranking_list = {}
    for key,value in outdict.items():
        for x in value:
            
            rank = getRank(topics_top_count[key], x[0])
            x.extend([rank])
            
            
    f = open('../data/tfidf.json', "w")
    f.write(json.dumps(outdict, indent=4))
    f.close()

def getRank(dictionary, word):
    num = dictionary[word]
    result = 0
    count_list = [x[1] for x in dictionary.items()]

    for i in range(len(count_list)):
        if count_list[i] > num:
            result += 1
    return result + 1

def tfidf(word, topics):
    # a dictionary with key: word, value: tfidf val
    d = dict()
    for w in word:
        # get the value of tf
        tf = word[w]
        # compute idf value
        idf = compute_idf(w, topics)
        d[w] = tf * idf
    # sort the dictionary by value in decreasing order
    output = dict()
    for idx, w in enumerate(sorted(d, key=d.get, reverse=True)):
        if idx >= 10:
            break
        output[w] = d[w]
    return output


def compute_idf(word, topics):
    # word: the given word we are interested in
    # topics: list of word-count dictionaries for each topic
    ct = 0
    for t in topics:
        if word in t:
            ct += 1
    return math.log(6/ct, 10)


def count_words(df, acc_dict):
    for w in df['tweets']:
        line = w.split()
        for el in line:
            if el == 'york' or el=='amp':
                continue
            if el not in acc_dict:
                acc_dict[el] = 1
            else:
                acc_dict[el] += 1

if __name__ == '__main__':
    main()

    # TODO:
    # print the rank of all top_ranked tfidf words in frequent words
    # print sentiment percentage -- Done
    # Graph sentiment percentage
    # Graph 6 tfidf top-ranked-word graphs