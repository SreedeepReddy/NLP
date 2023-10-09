# -*- coding: utf-8 -*-
"""Unsmoothed_Unigram_Bigram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TznhId1HFkTz9l8m4X4CtNqaOgnIiF8J
"""

import random
import re
from collections import defaultdict

# Step 1: Read text from "train.txt" file
with open('train.txt', 'r') as file:
    corpus = file.read()

# Preprocessing: Remove special characters except '.', ',', '!', and numbers
corpus = re.sub(r'[^a-zA-Z.,! ]', '', corpus)

# Step 2: Convert to lowercase and tokenize the text into words
corpus = corpus.lower()
words = corpus.split()

print(words)

# Step 3.1: Calculate unigram frequencies
word_freq = defaultdict(int)
for word in words:
    word_freq[word] += 1

# Step 3: Calculate bigram frequencies
bigram_freq = defaultdict(int)
for i in range(len(words) - 1):
    bigram = (words[i], words[i + 1])
    bigram_freq[bigram] += 1

print(bigram_freq)

# Step 4.1: Compute the probability distribution of words (unigram model)
total_words = len(words)
word_probs = {word: freq / total_words for word, freq in word_freq.items()}

# Step 4.2: Compute the probability distribution of bigrams (bigram model)
total_bigrams = len(words) - 1
bigram_probs = {(prev_word, word): freq / word_freq[prev_word] for (prev_word, word), freq in bigram_freq.items()}

#print(bigram_probs)

print("P(the|like) =", bigram_probs.get(("like", "the"), 0))
print("P(students|the) =", bigram_probs.get(("the", "students"), 0))

# Step 5.1: Generate random sentences using the unigram model
def generate_unigram_sentence():
    sentence = []
    while True:
        word = random.choices(list(word_probs.keys()), list(word_probs.values()))[0]
        if word == '.':
            if len(sentence) >= 2:
                break
            else:
                continue
        sentence.append(word)
    return ' '.join(sentence)

# Step 5.2: Generate random sentences using the bigram model
def generate_bigram_sentence():
    sentence = []
    while True:
        if not sentence:
            # Start with a random word as the first word
            word = random.choice(words)
            sentence.append(word)
        else:
            # Select the next word based on the previous word (bigram)
            prev_word = sentence[-1]
            next_word_candidates = [bigram[1] for bigram in bigram_probs if bigram[0] == prev_word]
            if not next_word_candidates:
                break  # If there are no valid next words, end the sentence
            word = random.choices(next_word_candidates, [bigram_probs[(prev_word, w)] for w in next_word_candidates])[0]
            sentence.append(word)

        if word == '.':
            break

    return ' '.join(sentence)

for _ in range(5):
    print(generate_unigram_sentence())
    print(generate_bigram_sentence())