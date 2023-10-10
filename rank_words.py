# This code will rank the 5-letter words inside the .txt database inside this project
# by how common they are, given a input book or article. Then, it will sort
# the words by this ranking, so the most common words come first to the game
# attempts.

import os
import PyPDF2
import pandas as pd
from database import WordDatabase
from primary_functions import *
import re

# initialize configurations
config = read_configurations()

# read file path as input from user
file_path = input("Write the path to the input string to rank the 5-letter words.")
if not(os.path.exists(file_path)):
    raise Exception("Could not find the file given to rank and sort words.")

# creating a pdf file object
pdfFileObj = open(file_path, 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)
input_text = ''

for i in range(len(pdfReader.pages)):
    page = pdfReader.pages[i]
    input_text+= page.extract_text()

# create one-column data frame all words form .txt database
wd = WordDatabase()
wd.read_database(config['paths']['words'])
df_words_rank = pd.DataFrame(
    {
        "Word": wd.word_database
    }
)
# dict_words_rank = {}
# for word in wd.word_database:
#     dict_words_rank[word]=len(re.findall(f'(?:(?<=[. -,])|(?<=^)){word}(?:(?=[, .-])|(?=$))',
#                                   input_text, re.IGNORECASE))

# Creates new column for each word to all occurrences on the input string
ranking_data\To Kill A Mockingbird - Full Text PDF.pdf
df_words_rank['Rank'] = df_words_rank['Rank'].astype('int64')

df_words_rank.sort_values(by=['Rank'])
print(df_words_rank)