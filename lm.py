# -*- coding: utf-8 -*-
"""
Julia Evans
Programming for CL
Final Project - lm.py

Implement LanguageModel class:
- train model using user-specified n
- generate ngrams for given input
- calculate ngram probabilities
- find most probable next word, given preceding ngram (if n > 1)
- generate text based on probabilities
"""
import random
import corpus

class LanguageModel(object):
    
    def __init__(self, n):
        # n: the number to be used for generating ngrams
        # counts: {(ngram) : {word : count}}
        # where count is the number of times word follows the ngram key
        # word_counts: {word : total # of instances of word}
        # count_words: {count : [word1, word2...]}
        # counts_prob: {count : probabilty of a word with that count}
        # vocabulary: types
        
        self.n = n
        self.counts = { }
        self.word_counts = { }
        self.count_words = { }
        self.counts_prob = { }
        self.vocabulary = set()

    
    def __str__(self):
        info = ['N:', str(self.n), '\nCounts:', str(len(self.counts)), '\nWord_Counts:', str(len(self.word_counts))]
        return ' '.join(info)

        
    def train(self, sequences):
        # sequences: a list of lists of tokens
        # for each list within sequences:
        # if self.n > 1 (= bigrams or larger):
        # call get_ngrams to generate a list of ngrams (seq)
        # update counts with ngrams of length n-1 from seq
        # and the words that follow each ngram
        # update vocabulary with words from seq (types)
        # update word_counts with words from seq and # of instances (tokens)
        # if unigrams:        
        # update word_counts with words from lst and # of instances
        # update count_words by switching word_counts keys and values 
        # unigram_stats: {count : # of words with that count}
        
        if self.n > 1:
            for lst in sequences:
                seq = get_ngrams(lst, self.n)
                for tpl in seq:
                    ngram = tpl[:self.n - 1]
                    word = tpl[self.n - 1]
                    if ngram in self.counts:
                        ngram_d = self.counts[ngram]
                        if word in ngram_d:
                            ngram_d[word] += 1
                        else:
                            ngram_d[word] = 1
                    else:
                        self.counts[ngram] = {word : 1}
                        
                self.vocabulary.update([word for word in lst])
            
            for value in self.counts.values():
                for k, v in value.items():
                    self.word_counts.setdefault(k, 0)
                    self.word_counts[k] += v
            
        else:
            for lst in sequences:
                for word in lst:
                    self.word_counts.setdefault(word, 0)
                    self.word_counts[word] += 1
            
            for word in self.word_counts:
                count = self.word_counts[word]
                self.count_words.setdefault(count, [ ]).append(word)
                
            unigram_stats = { }
            for count in self.count_words:
                unigram_stats[count] = (count * len(self.count_words[count]))
                
            self.counts_prob = normalize(unigram_stats)
     
           
    def p_next(self, tokens):
        # tokens: list of strings (the text so far)
        # finds the estimated probability distribution for the next word 
        # following the given sequence of tokens
        # returns a dictionary: {word : relative probability of word}
        
        pad = [None] * (self.n - 1)
        tokens = pad + tokens     
        i = self.n - 1
        test_gram = tuple(tokens[-i:])
        
        return normalize(self.counts[test_gram])
        
        
    def generate(self):
        # generates random token sequence according to probs from training
        # returns list of tokens (strings)     
        
        my_sequence = [ ]
        
        if self.n > 1:
            next_word = sample(self.p_next(my_sequence))
            my_sequence.append(next_word)
            
            while next_word != None:  
                next_word = sample(self.p_next(my_sequence))
                my_sequence.append(next_word)
                
        else:
            count = sample(self.counts_prob)
            next_word = random.choice(self.count_words[count])
            my_sequence.append(next_word)
            
            while next_word not in '.?!':
                count = sample(self.counts_prob)
                next_word = random.choice(self.count_words[count])
                my_sequence.append(next_word)
        
        return [word for word in my_sequence if word != None]
 
    
def get_ngrams(tokens, n):
    # tokens: list of tokens (strings)
    # generates ngrams of length n from the list of tokens
    # pads the list so every token is in an equal number of ngrams
    # returns a list of tuples [(ngram), (ngram)...]
       
    if tokens != [ ]:
        pad = [None] * (n - 1)
        tokens = pad + tokens + pad
        return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]    
    else:
        return [ ]
    

def normalize(word_counts):
    # generates a dictionary of word probabilities
    # word_probabilities: {word : (# of word instances)/(# of tokens)}
    
    total = sum(word_counts.values())
    word_probabilities = {k : (v / total) for k, v in word_counts.items()}
    
    return word_probabilities


def laplace_normalize(word_counts, vocabulary):
    # generates a dictionary of word probabilities using Laplace smoothing
    # way of accounting for previously unseen ngrams, so prob is not 0
    # word_probabilities: {word : (# of word instances + 1)/(# of tokens + v)}
    
    total = sum(word_counts.values())
    word_probabilities = {k : ((v + 1) / (total + len(word_counts))) for k, v in word_counts.items()}
        
    return word_probabilities


def sample(distribution):
    # distribution: {word : probability of word}
    # gets a random number between 0 - 1
    # converts the word probabilities to distributions between 0 - 1
    # returns key with distribution containing the random number
    
    dist_list = [[k, v] for k, v in distribution.items()]
    current_prob = random.random() 
    increment = 0
    
    for i in dist_list:
        increment += i[1]        
        if increment >= current_prob:
            return i[0]
