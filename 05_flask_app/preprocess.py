import numpy as np
import codecs
import unidecode
import re
import ftfy
import html
import emoji
import spacy
from nltk.tokenize import WordPunctTokenizer
from spacy.lang.en.stop_words import STOP_WORDS
tok = WordPunctTokenizer()
nlp = spacy.load('en', disable=['parser', 'tagger', 'ner'])
nlp.Defaults.stop_words.add("rt")


pattern_retweet = r'^rt '
pattern_char = r'@[A-Za-z0-9_]+'
pattern_html = r'https?://[^ ]+'
pattern_combi = r'|'.join((pattern_char, pattern_html))
pattern_www = r'www.[^ ]+'
negations_dic = {"ain't": "is not", "aren't": "are not","can't": "cannot",
                   "can't've": "cannot have", "'cause": "because", "could've": "could have",
                   "couldn't": "could not", "couldn't've": "could not have","didn't": "did not",
                   "doesn't": "does not", "don't": "do not", "hadn't": "had not",
                   "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not",
                   "he'd": "he would", "he'd've": "he would have", "he'll": "he will",
                   "he'll've": "he will have", "he's": "he is", "how'd": "how did",
                   "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
                   "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
                   "I'll've": "I will have","I'm": "I am", "I've": "I have",
                   "i'd": "i would", "i'd've": "i would have", "i'll": "i will",
                   "i'll've": "i will have","i'm": "i am", "i've": "i have",
                   "isn't": "is not", "it'd": "it would", "it'd've": "it would have",
                   "it'll": "it will", "it'll've": "it will have","it's": "it is",
                   "let's": "let us", "luv" : "love", "ma'am": "madam", "mayn't": "may not",
                   "might've": "might have","mightn't": "might not","mightn't've": "might not have",
                   "must've": "must have", "mustn't": "must not", "mustn't've": "must not have",
                   "needn't": "need not", "needn't've": "need not have", "n't" : "not", "o'clock": "of the clock",
                   "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
                   "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would",
                   "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have",
                   "she's": "she is", "should've": "should have", "shouldn't": "should not",
                   "shouldn't've": "should not have", "so've": "so have","so's": "so as",
                   "this's": "this is",
                   "that'd": "that would", "that'd've": "that would have","that's": "that is",
                   "there'd": "there would", "there'd've": "there would have","there's": "there is",
                       "here's": "here is",
                   "they'd": "they would", "they'd've": "they would have", "they'll": "they will",
                   "they'll've": "they will have", "they're": "they are", "they've": "they have",
                   "to've": "to have", "ur" : "your", "wasn't": "was not", "we'd": "we would",
                   "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have",
                   "we're": "we are", "we've": "we have", "weren't": "were not",
                   "what'll": "what will", "what'll've": "what will have", "what're": "what are",
                   "what's": "what is", "what've": "what have", "when's": "when is",
                   "when've": "when have", "where'd": "where did", "where's": "where is",
                   "where've": "where have", "who'll": "who will", "who'll've": "who will have",
                   "who's": "who is", "who've": "who have", "why's": "why is",
                   "why've": "why have", "will've": "will have", "won't": "will not",
                   "won't've": "will not have", "would've": "would have", "wouldn't": "would not",
                   "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
                   "y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have", "yo" : "you",
                   "you'd": "you would", "you'd've": "you would have", "you'll": "you will",
                   "you'll've": "you will have", "you're": "you are", "you've": "you have", "yu" : "you" }
pattern_neg = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def clean(input_text):
    #print("raw text: \n{} \n".format(input_text))
    decoded = ftfy.fix_encoding(input_text)
    no_html = html.unescape(decoded)
    #print("decoded: \n{} \n".format(decoded))
    #emojiesed = emoji.emojize(decoded)
    #print("emojiesed: \n{} \n".format(emojiesed))
    lower = decoded.lower()
    #print("lower: \n{} \n".format(lower))
    tr_free = re.sub(pattern_retweet, '', lower)
    html_free = re.sub(pattern_combi, '', tr_free)
    url_free = re.sub(pattern_www, '', html_free)
    #print("html and url free: \n{}\n".format(url_free))
    demo = emoji.demojize(url_free)
    try:
        decoded = unidecode.unidecode(codecs.decode(demo, 'unicode_escape'))
        #print("decoded try: \n{}".format(decoded))
    except:
        decoded = unidecode.unidecode(demo)
        #print("decoded except: \n{}".format(decoded))
    apostrophe_handled = re.sub("’", "'", decoded)
    #print("apostrophe_handled: \n{}".format(apostrophe_handled))
    expanded = pattern_neg.sub(lambda x: negations_dic[x.group()], apostrophe_handled)
    #print("expanded: \n{}".format(expanded))
    spell_corrected = re.sub(r'(.)\1+', r'\1\1', expanded)
    return spell_corrected

def remove_signs(input_text):
    letters_only = re.sub("[^a-zA-Z]", " ", input_text)
    n_rt = re.sub(pattern_retweet, ' ', letters_only)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tok.tokenize(n_rt) if len(x) > 1]
    #stemmed = [x for x  in stemmer.stem(words)]
    #stemmed = [stemmer.stem(word) for word in words]
    #print(stemmed)
    #print(words)
    return (" ".join(words)).strip()

def lemm(input_text):
    doc = nlp(input_text)
    # Extract the lemma for each token and join
    return(" ".join([token.lemma_ for token in doc]))

def remove_stopwords(input_text, stopword_list=STOP_WORDS):
    '''a function for removing the stopword'''
    # removing the stop words and lowercasing the selected words
    text = [word.lower() for word in input_text.split() if word.lower() not in stopword_list]
    # joining the list of words with space separator
    return " ".join(text)
