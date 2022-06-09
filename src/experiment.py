import nltk
from nltk import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

if __name__ == '__main__':
    lemmetizer = WordNetLemmatizer()
    word = lemmatizer.lemmatize('doses', 'n')
    print(word)