import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import acquire
from time import strftime

import warnings
warnings.filterwarnings('ignore')

def basic_clean(string):
    '''
    This function takes in a string and returns a normalized version of it.
    '''
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    string = re.sub(r'[^\w\s]', '', string).lower()
    return string

def tokenize(string):
    '''
    This function takes in a string and tokenizes it.
    '''
    # create tokenizer object
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # apply tokenizer
    string = tokenizer.tokenize(string, return_str = True)
    return string

def stem(string):
    '''
    This function takes in a string and returns a string with those words stemmed.
    '''
    # create stemmer object
    ps = nltk.porter.PorterStemmer()
    # stem each word in list of words
    stems = [ps.stem(word) for word in string.split()]
    # join lists of words into string, assign to variable
    string = ' '.join(stems)
    return string

def lemmatize(string):
    '''
    This function takes in a string and returns a string with those words lemmatized.
    '''
    # create lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()   
    # lemmatize each word in list of words
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # join list of words into string, assign to variable
    string = ' '.join(lemmas) 
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, extra_words and exclude_words (default empty lists)
    and returns a string with stopwords removed.
    '''
    # create list of stopwords
    stopword_list = stopwords.words('english')  
    # remove exclude_words from stopword_list
    stopword_list = set(stopword_list) - set(exclude_words)
    # add extra_words to stopword_list
    stopword_list = stopword_list.union(set(extra_words))
    # split words in string
    words = string.split()
    # list words from string with stopwords removed, assign to variable
    filtered_words = [word for word in words if word not in stopword_list]
    # join remaining words, assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords

def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function takes in a dataframe, a column name, and extra_words/exclude_words
    for removing stopwords and returns the dataframe with the article title, its
    original contents, as well as cleaned, stemmed, lemmatized, and tokenized
    versions of its contents with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)   
    df['stemmed'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(stem)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    df['lemmatized'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]