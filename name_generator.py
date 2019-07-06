import random
import string
import sys
from collections import defaultdict
VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

def name():
    length = random.randint(3,8)
    name = ''
    i = 0
    while i < length:
        letter = ''
        r = random.random()
        if i % 2 == 0:
            if r < .95:
                letter = random.choice(CONSONANTS)
                if letter in ['x', 'q', 'j', 'z']:
                    if random.random() < .5:
                        letter = random.choice(CONSONANTS)
                if letter == 't':
                    if random.random() < .4:
                        letter = 'th'
                if letter == 'q':
                    letter = 'qu'
            else:
                letter = random.choice(VOWELS)
                i -= 1
        else:
            if r < .95:
                letter = random.choice(VOWELS)
            else:
                letter = random.choice(CONSONANTS)
                i -= 1
        name += letter
        i += 1
    return name.capitalize()
