# features

def character_ngrams(text, n=2):
    ngrams = []
    for i in range(len(text) - (n-1)):
        ngrams.append(text[i:i+n])
    return ngrams

def word_ngrams(text, n=2):
    words = text.split(' ')
    ngrams = []
    for i in range(len(words) - (n-1)):
        ngrams.append(' '.join(words[i:i+n]))
    return ngrams
