# -*- coding: utf-8 -*-
"""
Julia Evans
Programming for CL
Final Project - main.py

This module is responsible for user interaction.

Users can:
- create a new language model with user-specified n
- load texts from a file
- train language model on those texts
- generate and print texts
- write texts to a file
- compare different ngram model outputs
- find the most frequent ngrams in a model
- exit the program
"""
import corpus
import lm


def get_choice():
    
    print('\nWhat would you like to do?'
      '\nPress G to generate text.'
      '\nPress C to compare output from different ngram models.'
      '\nPress M to get the most frequent ngrams of your language model.'
      '\nPress T to train the model with another file.'
      '\nPress N to create a new language model.'
      '\nPress Q to quit.')    
    return input('Enter choice: ').lower()


def get_generate():
    print('\nThis is the fun part. How many texts would you like?')
    txt_num = int(input('Enter number of texts: ' ))
        
    print('\nGot it! And where would you like your texts?'
          '\nPress C to print to the console, or press F to save to a file.')
    file_dest = input('Enter C or F: ').lower()

    if file_dest == 'c':
        for n in range(txt_num):
            gen_txt = model.generate()
            print('\n', corpus.detokenize(gen_txt))       

    elif file_dest == 'f':
        file = open('new_shakespeare.txt', 'a+')
        file.write('Ngram model: ' + str(model.n) + '\nTraining file: ' + filename + '\n' + '\n')
        for n in range(txt_num):
            gen_txt = model.generate()
            file.write(corpus.detokenize(gen_txt) + '\n' + '\n')
        file.close()
        print('\nYour file is ready! Please check new_shakespeare.txt.') 
    return get_choice()


def get_trainer():
    print('\nPlease enter the name of a file to use for training.')
    filename = input('Enter file name: ')
    tokens = corpus.tokenize(corpus.read_file(filename))
    model.train(tokens)
    return get_choice()


def get_new_model():
    global model, filename
    print('\nPlease enter a number n to select ngrams type.')
    n = int(input('Enter n: '))
    model = lm.LanguageModel(n)
    
    print('\nNice choice!'
          '\nNow, please enter the name of a file to use for training.')
    filename = input('Enter file name: ')
    tokens = corpus.tokenize(corpus.read_file(filename))
    model.train(tokens)
    return get_choice()


def get_comparison():
    m1 = lm.LanguageModel(1)
    m2 = lm.LanguageModel(2)
    m3 = lm.LanguageModel(3)
    
    print('\nGreat. Now, please enter the name of a file to use for training.')
    filename = input('Enter file name: ')
    tokens = corpus.tokenize(corpus.read_file(filename))
    m1.train(tokens)
    m2.train(tokens)
    m3.train(tokens)
    
    print('\nThis should be interesting. How many texts would you like?')
    txt_num = int(input('Enter number of texts: ' ))
  
    for i in range(txt_num):
        m1_txt = m1.generate()
        print('\nUnigram generated text:\n', corpus.detokenize(m1_txt))
        m2_txt = m2.generate()
        print('\nBigram generated text:\n', corpus.detokenize(m2_txt))
        m3_txt = m3.generate()
        print('\nTrigram generated text:\n', corpus.detokenize(m3_txt))
    
    return get_choice()


def take_first(elem):
    return elem[0]

def get_most_frequent():
    if model.n == 1:
        ngram_freq = [[v, k] for k, v in model.word_counts.items()]
        ordered_freq = sorted(ngram_freq, reverse=True)
        print('\nMost frequent unigrams:')
        for freq in ordered_freq[:10]:
            print(freq)
    else:
        ngram_freq = [ ]
        for k, v in model.counts.items():
            for key, val in v.items():
                ngram = k + (key,)
                ngram_freq.append([val, ngram])
        ordered_freq = sorted(ngram_freq, key=take_first, reverse=True)
        print('\nMost frequent ' + str(model.n) + 'grams:')
        for freq in ordered_freq[:10]:
            print(freq)
    
    return get_choice()
    

print('Hello!  Welcome to language model training!'
      '\nTo begin, now please enter a number n to select ngrams type.')
n = int(input('Enter n: '))
model = lm.LanguageModel(n)

print('\nNice choice!'
      '\nNow, please enter the name of a file to use for training.')

filename = input('Enter file name: ')
tokens = corpus.tokenize(corpus.read_file(filename))
model.train(tokens)
print('\nGreat, we\'re ready to begin!') 

choice = get_choice()

while choice != 'q':
    if choice == 'g':
        choice = get_generate()
    elif choice == 'c':
        choice = get_comparison()
    elif choice == 'm':
        choice = get_most_frequent()
    elif choice == 't':
        choice = get_trainer()
    elif choice == 'n':
        choice = get_new_model()      
    else:
        print('\nSorry, I didn\'t understand that. Let\'s try again.')
        choice = get_choice()
    
print('\nThat was fun! Goodbye~')