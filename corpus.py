# -*- coding: utf-8 -*-
"""
Julia Evans
Programming for CL
Final Project - corpus.py

Read text files, process, tokenize and detokenize text.
"""
from nltk.tokenize import word_tokenize, sent_tokenize
from sacremoses import MosesDetokenizer
#from nltk.tokenize.treebank import TreebankWordDetokenizer


def read_file(filename):
    txt = ''
    with open(filename) as file:
        txt += file.read()
    return txt


def tokenize(text):
    # takes a string and returns a list of lists of tokens
    # each inner list contains one sentence
    
    sent_list = sent_tokenize(text)
    tokens = [word_tokenize(sent.lower()) for sent in sent_list]
    return tokens


def detokenize(tokens):
    # takes a list of tokens and returns a single string

    detokenizer = MosesDetokenizer()
    return detokenizer.detokenize(tokens, return_str=True).capitalize()

#    detokenizer = TreebankWordDetokenizer()
#    return detokenizer.detokenize(tokens).capitalize()
