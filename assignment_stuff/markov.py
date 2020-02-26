from dictogram import Dictogram


class MarkovChain:
    def __init__(self, word_list):
         self.markov_chain = self.build_markov(word_list)
         self.first_word = list(self.markov_chain.keys())[0]

    def build_markov(self, word_list):
        markov_chain = {}
        for i in range(len(word_list) - 1):
            #get the current word and the word after
            current_word = word_list[i]
            next_word = word_list[i+1]
            if current_word in markov_chain.keys(): #already there
                markov_chain[current_word].add_count(next_word)
            else: #first entry
                markov_chain[current_word] = Dictogram([next_word])
        return markov_chain

    def walk(self, num_words):
        result = [self.first_word]
        for _ in range(num_words-1):
            result.append(self.markov_chain[result[-1]].sample())
        return ' '.join(result)

    def print_chain(self):
        for word, histogram in self.markov_chain.items():
            print(word, histogram)


markov_chain = MarkovChain(["one", "fish", "two", "fish", "red", "fish", "blue", "fish"])
markov_chain.print_chain()
print(markov_chain.walk(10))
