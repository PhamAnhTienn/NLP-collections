import streamlit as st 
import pandas as pd
import numpy as np
import re
from collections import Counter
import string

def read_corpus(filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        line = file.readlines()
        
        words = []
        for word in line:
            words += re.findall(r'\w+', word.lower())
        return words
    
corpus = read_corpus("corpus.txt")
vocab = set(corpus)
words_count = Counter(corpus) 
total_words = float(sum(words_count.values()))
word_probs = { word : words_count[word]/total_words for word in words_count.keys() }

def split(word):
    return [ (word[:i], word[i:])  for i in range(len(word) + 1)]

def delete(word):
    return [left + right[1:] for left, right in split(word) if right]

def swap(word):
    return [left + right[1] + right[0] + right[2:] for left, right in split(word) if len(right) > 1 ]

def replace(word): 
    return [left + center + right[1:] for left, right in split(word) if right for center in string.ascii_lowercase]

def insert(word): 
    return [left + center + right[1:] for left, right in split(word) for center in string.ascii_lowercase]

def one_edits(word):
    return set((delete(word) + swap(word) + replace(word) + insert(word)))

def two_edits(word):
    return set(e2 for e1 in one_edits(word) for e2 in one_edits(e1))

def correct_spelling(word, vocab, word_probs):
    if word in vocab:
        return f"{word} is already corrected"
    
    suggestions = one_edits(word) or two_edits(word) or [word]
    best_guesses = [ w for w in suggestions if w in vocab ]
    
    if not best_guesses:
        return f"Sorry, no suggestions found for {word}"
    
    suggestions_with_probs = [(w, word_probs[w]) for w in best_guesses]
    suggestions_with_probs.sort(key=lambda x: x[1], reverse=True)
    return f"Suggestions for {word}: " + ', '.join([f"{w} ({prob:.2%})" for w, prob in suggestions_with_probs[:10]])

st.title("AutoCorrect Misspelled Word")
word = st.text_input('Search Here')

if st.button("Check"):
    result = correct_spelling(word, vocab, word_probs)
    st.write(result)