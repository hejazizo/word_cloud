import codecs
import json
import os
from collections import Counter
from os import path
from pathlib import Path
from pprint import pprint

import arabic_reshaper
import numpy as np
from bidi.algorithm import get_display
from hazm import *
from PIL import Image
from tqdm import tqdm
from wordcloud import WordCloud

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
with Path('./insta.txt').open() as f:
    text = f.read()

# remove stop words
with open('./stop_words.txt') as f:
    stop_words = f.read().split('\n')

tokens = word_tokenize(text)
tokens = [w for w in tokens if w not in stop_words]
text = ' '.join(tokens)

# Read the whole text.
# f = codecs.open(os.path.join(d, 'arabicwords.txt'), 'r', 'utf-8')
pprint(Counter(tokens).most_common(100))
with open('./stats.txt', 'w') as f:
    most_common = [f'{w[0]}: {w[1]}' for w in Counter(tokens).most_common(100)]

    f.write('\n'.join(most_common))

print('Stats Done.')
# Make text readable for a non-Arabic library like wordcloud
text = arabic_reshaper.reshape(text)
text = get_display(text)


# alice_mask = np.array(Image.open(path.join(d, "/home/ali/maple.jpg")))
# Generate a word cloud image
wordcloud = WordCloud(
    background_color="white",
    # mask=alice_mask,
    width=500, height=900,
    font_path='fonts/NotoNaskhArabic/NotoNaskhArabic-Regular.ttf').generate(text)

# Export to an image
wordcloud.to_file("uofa-square.png")
print('DONE.')
