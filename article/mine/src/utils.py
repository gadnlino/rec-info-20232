from tokenizers import Tokeniser
from datetime import datetime

tokeniser = Tokeniser()

#https://stackoverflow.com/questions/31539243/are-twitters-id-time-ordered
def get_tweet_creation_date(tid):
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    utcdttime = datetime.utcfromtimestamp(tstamp/1000)
    #print(str(tid) + " : " + str(tstamp) + " => " + str(utcdttime))

    return utcdttime

def project(array, prop):
    return list(map(lambda x: x[prop], array))

def get_summary(text):
    sentences = tokeniser.sent_tokenise(text)
    useful = sentences[0:2] if len(sentences) > 2 else sentences
    return ''.join(useful)

def get_token_count(text):
    return len(set(tokeniser.tokenise(text)))

def get_token_count(text):
    return len(set(tokeniser.tokenise(text)))

def get_distinct_token_count(list):
    tokens = set()

    for d in list:
        tokens = tokens.union(tokeniser.tokenise(d))
    
    return len(tokens)