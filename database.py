import re


class WordDatabase:
    def __init__(self):
        self.words = []

    def read_database(self,path):
        words_file = open(path,"r")
        five_letter_words=list(
            filter(
                lambda x: len(x)==6,words_file.readlines()
                ))
        self.word_database=list(map(lambda x: x.replace('\n', ''), five_letter_words))

    def update_database_by_query(self, query):
        
        self.words = list(re.findall(query))

    def get_most_relevant_word(self):
        return self.words[0]