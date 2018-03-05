#!/usr/bin/env python3

import random

order = 4
ngrams = {}


class TweetGenerator():
    # tweet generator with markov chain algorithm
    def __init__(self, txt):
        self.txt = txt

    def setup(self, txt):
        for i in range(0, len(txt) - order):
            gram = txt[i:i + order]
            if gram not in ngrams:
                ngrams[gram] = []
            ngrams[gram].append(txt[i + order])
        currentGram = txt[0:order]
        result = currentGram

        for i in range(0, 75):
            possibilities = ngrams[currentGram]
            if(not possibilities):
                break
            next = random.choice(possibilities)
            result += next
            currentGram = result[len(result) - order:len(result)]
        return(result)
