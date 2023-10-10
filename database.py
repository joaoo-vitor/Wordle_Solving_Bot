import re


class WordDatabase:
    def read_database(self,path):
        words_file = open(path,"r")
        five_letter_words=list(
            filter(
                lambda x: len(x)==6,words_file.readlines()
                ))
        self.word_database=list(map(lambda x: x.replace('\n', ''), five_letter_words))

    def update_database_by_query(self, query):
        # add space the the end of the query to consider the separation of words
        query+='\n'

        # make query and update list of words
        words_before = len(self.word_database)
        self.word_database = list(re.findall(query, '\n'.join(self.word_database)))
        words_after = len(self.word_database)
        print(f'Removed {words_before-words_after} words from database after query.')

        # if there are no more words after query, throw an exception
        if len(self.word_database)==0:
            raise Exception("There are no words left in the database to be attempted.")

    def get_most_relevant_word(self):
        return self.word_database[0]
    
    def remove_fist_word(self):
        # if there are no more words after removal, throw an exception
        if len(self.word_database)==0:
            raise Exception("There are no words left in the database to be attempted.")
        del self.word_database[0]

    