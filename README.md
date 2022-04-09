# Shakespearean Text Generator

This Shakespearean text generator was built by Julia Evans for a programming class at the IMS, University of Stuttgart.

## Packages

This program requires the following packages:
- random
- nltk
- sacremoses

## Usage

Users can access all the functionality of the language model through main.py. 

Upon running main, the user will be prompted to enter an *n* for ngrams and then a file to use for training. 

After the language model has been created and trained using this input, the user is given the following options: 

- Generate text
- Compare output from different ngram models
- Find the most frequent ngrams for the model
- Train the model with an additional text
- Create a new model
- Quit

When users choose to generate text, they will also be prompted to choose the number of texts and where to put the text, i.e. print to the console or write to a file.  ("One text" in this context is defined as one sentence.)