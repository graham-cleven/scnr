#!/usr/bin/env python3

import nltk
from nltk.stem.lancaster import LancasterStemmer
from NLP import classifier_data

stemmer = LancasterStemmer()


def classifier(query=None):
    training_data = classifier_data.get_traning_data()

    # capture unique stemmed words in the training corpus
    corpus_words = {}
    class_words = {}
    # turn a list into a set (of unique items) and then a list again (this removes duplicates)
    classes = list(set([a["class"] for a in training_data]))
    for c in classes:
        # prepare a list of words within each class
        class_words[c] = []

    # loop through each sentence in our training data
    for data in training_data:
        # tokenize each sentence into words
        for word in nltk.word_tokenize(data["sentence"]):
            # ignore a some things
            if word not in ["?", "'s"]:
                # stem and lowercase each word
                stemmed_word = stemmer.stem(word.lower())
                # have we not seen this word already?
                if stemmed_word not in corpus_words:
                    corpus_words[stemmed_word] = 1
                else:
                    corpus_words[stemmed_word] += 1

                # add the word to our words in class list
                class_words[data["class"]].extend([stemmed_word])

    # calculate a score for a given class
    def calculate_class_score(query, class_name, show_details=True):
        score = 0
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(query):
            # check to see if the stem of the word is in any of our classes
            if stemmer.stem(word.lower()) in class_words[class_name]:
                # treat each word with same weight
                score += 1
        return score

    scores = []
    # now we can find the class with the highest score
    for c in class_words.keys():
        scores.append({"class": c, "score": calculate_class_score(query, c)})
    return sorted(scores, key=lambda b: b["score"], reverse=True)
