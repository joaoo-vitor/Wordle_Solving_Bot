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
fileObj = open(file_path, 'rb')
 
if fileObj.name.endswith(".pdf"):
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(fileObj)
    input_text = ''

    for i in range(len(pdfReader.pages)):
        page = pdfReader.pages[i]
        input_text+= page.extract_text()
elif fileObj.name.endswith(".txt"):
    input_text = str(fileObj.read())
else:
    raise Exception("The file termination wasn't on the list.")


# create one-column data frame all words form .txt database
wd = WordDatabase()
wd.read_database(config['paths']['words'])
print(f'Read a total of {len(wd.word_database)} words from the txt file. called \'{config["paths"]["words"]}\'')
df_words_rank = pd.DataFrame(
    {
        "Word": wd.word_database
    }
)

# Creates new column for each word to all occurrences on the input string
list_rank = []
for index, row in df_words_rank.iterrows():
    list_rank.append(len(re.findall(f'(?:(?<=[. -,])|(?<=^)){row.Word}(?:(?=[, .-])|(?=$))',
                                 input_text, re.IGNORECASE)))
    pct = 100*index/len(df_words_rank)
    print(f'Analyzing file... {pct:.2f}% ', end='\r')

df_words_rank['Rank'] = list_rank
df_words_rank['Rank'] = df_words_rank['Rank'].astype('int64')

# sort values by Ranking
df_words_rank.sort_values(by=['Rank'],ascending=False, inplace=True)

# write whole dataframe to excel
df_words_rank.to_excel(r'File_name.xlsx', index=False)

# write txt file with list of words 
# write to data.txt
with open('words_alpha1.txt', 'w') as f:
   f.write(
       '\n'.join(df_words_rank['Word'].to_list())
   )
print(f'Rewrote txt file with list of {len(df_words_rank)} words.')
