# Tokenizador de documentos
# Converte uma entrada de textos para bigramas, analise semantica ou expansao de query
from flask import Flask
from flask import request
from flask import jsonify

import re
import os
import sys

import spacy
from spacy.lang.en import stop_words
import nltk
import json
import pickle
from scipy import spatial

from nltk import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from gensim.models.phrases import Phraser

nltk.download('stopwords')
nltk.download('punkt')

STOPWORDS = stopwords.words("english")

class Tokeniser(object):

    def __init__(self):
        self.porter = PorterStemmer()
        self.stop_words = STOPWORDS

    def tokenise(self, text, min_token_length=3):
        '''
        Tokenises a string of text by keeping only alphabetic characters.
        Returns a list of tokens.
        '''

        tokens = [self.porter.stem(w.lower()) for w in word_tokenize(text) if w not in self.stop_words]
        alphabet_regex = re.compile('[a-zA-Z]+')
        filtered_tokens = [t for t in tokens if alphabet_regex.match(t) and len(t) >= min_token_length]

        return filtered_tokens
    
    def sent_tokenise(self, text):
        return sent_tokenize(text)

class GencyTokeniser(object):

    def __init__(self):

        nlp = spacy.load("en_core_web_sm")
        self.nlp = nlp
        self.stop_words = STOPWORDS
        self.bigram_model = Phraser.load('C:\\Users\\guiav\\Source_Code\\repos\\rec-info-20232\\article\\Dissertation_axelSuarez-master\\Dissertation-master\\node_endpoints\\python_scripts\\bigram_model')

    def is_useful_token(self, token):
        # 90 = part_of_speech:NUM
        return token.is_alpha or (token.pos == 90)

    def apply_phrase_models(self, tokens):
        text = self.bigram_model[tokens]
        return [token for token in text if token not in self.stop_words]
        #return [token for token in text]

    def tokenise(self, text):
        all_tokens = []
        for sentence in self.nlp(text).sents:
            tokens = [token.lemma_ for token in sentence if self.is_useful_token(token)]
            all_tokens += self.apply_phrase_models(tokens)
        return all_tokens

    
        

    def bigrams(self, text):
        tokenized_text = self.tokenise(text)
        return [x for x in tokenized_text if "_" in x]

# trained_tokenizer = GencyTokeniser()
# simple_tokenizer = Tokeniser()

# @app.route('/semantic', methods=['GET','POST'])
# def semantic():
#     token_sent = trained_tokenizer.tokenise(request.form['text_query'])
#     if not token_sent: return jsonify(token_sent)
#     token_sent = list(filter(lambda x: x in word2vec.vocab, token_sent))
#     central_vector = sum([word2vec[token] for token in token_sent])/len(token_sent)
#     similarities = [(1 - spatial.distance.cosine(word2vec[token],central_vector), token) for token in token_sent]
#     return jsonify([x[1] for x in sorted(similarities, key=lambda tup: tup[0], reverse=True)[:10]])

# @app.route('/expansion', methods=['GET','POST'])
# def expansion():
#     token_sent = trained_tokenizer.tokenise(request.form['text_query'])
#     if not token_sent: return jsonify(token_sent)
#     token_sent = list(filter(lambda x: x in word2vec.vocab, token_sent))
#     central_vector = sum([word2vec[token] for token in token_sent])/len(token_sent)
#     similarities = [(1 - spatial.distance.cosine(word2vec[token],central_vector), token) for token in token_sent]
#     top_10 = [x[1] for x in sorted(similarities, key=lambda tup: tup[0], reverse=True)[:10]]
#     similar_top_10 = [word2vec.most_similar(positive=token, topn=1)[0][0] for token in top_10]
#     return jsonify(top_10 + similar_top_10)