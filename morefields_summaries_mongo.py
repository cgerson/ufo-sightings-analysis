import re
import string
from nltk.tokenize import wordpunct_tokenize
import nltk.data
from nltk.corpus import stopwords
from pymongo import MongoClient
import sys
#sys.path.insert(0, './text2num/')
import text2num
tok = nltk.data.load('tokenizers/punkt/english.pickle') #sentence splitting

stops = set(stopwords.words("english")) #faster to search a set

def nums(x):
    try:
        result = text2num.text2num(x)
    except:
        result = x
    return result

#bag of words
def summary_to_list(text):   
    bag_of_words = []
    no_numbers = re.sub("\d+", " ", text) #no numbers
    no_notes = re.sub("\(\(.*\)\)", " ", no_numbers) #remove NUFORC notes
    words = wordpunct_tokenize(expandContractions(no_notes.lower()))
    #expand contractions and tokenize
    filt = filter(lambda token: token not in string.punctuation \
                  and token not in stops \
                  and nums(token)==token, words) #remove stopwords and digits
    joined = " ".join(filt)
    bag_of_words.append(joined)
    return bag_of_words

#prep word2vec, sentences with numbers and stopwords
def summary_to_sent(text):
    no_notes = re.sub("\(\(.*\)\)", " ", text) #remove NUFORC notes
    raw_sentences = tok.tokenize(no_notes.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            #no_numbers = re.sub("\d+", " ", raw_sentence) #no numbers
            words = wordpunct_tokenize(expandContractions(raw_sentence.lower()))
            filt = filter(lambda token: token not in string.punctuation, words) #remove punctuation
            try:
                to_digits = [str(nums(x)) for x in filt]
            except:
                to_digits = filt
            sentences.append(to_digits)
    return sentences

#script to extract adjectives from text
def adjs(sent):  
    adj = []
    for s in sent:
        tagged = nltk.pos_tag(s)
        adj.extend(filter(lambda w: w[1]=="JJ", tagged))
    return adj

cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "i'd": "i would",
  "i'd've": "i would have",
  "i'll": "i will",
  "i'll've": "i will have",
  "i'm": "i am",
  "i've": "i have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text)


client = MongoClient(host="54.69.198.239",port=27017)
db = client.UFO
col = db.Summaries

def update_docs():
    for doc in col.find():
        print doc['_id']
        text = doc['text']
        bag_of_words = summary_to_list(text)
        sentences = summary_to_sent(text)
        adj_sent = adjs(sentences)
        col.update_one({'_id':doc['_id']}, {"$set": {"bag_of_words":bag_of_words,
                                    "word_2_vec_sentences":sentences,
                                   "adj":adj_sent}})












