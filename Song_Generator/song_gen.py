from operator import itemgetter
from random import randint, random
from re import sub, findall
from sys import argv, exit
import time


'''
"\n\n" --> 'END_STANZA'
"\n" --> 'END_BAR'
"*********" --> 'END_SONG'
"<repeated stanza>" --> 'REPEAT_STANZA_<NUM>'
'''


class Histogram:
    def __init__(self, source_text, flag=''):
        self.word_list = None

        # set the flag to 'F' to load text from a file
        if flag.lower() == 'f':
            source_text = histogram_file(source_text)

        # To load from a word_list or string, don't pass in a flag.
        self.word_list = get_word_list(source_text)

        self.histogram = get_histogram(self.word_list)

        self.total_tokens = get_total_tokens(self.histogram)
        self.total_types = unique_words(self.histogram)

        self.avg_stanza_len = []
        self.avg_song_len = []
        self.avg_stanza_num = []

        self.markov_chain = markov(self.word_list)


def get_word_list(source_text):
    ''' Splits text_str into a list of lowercase words
        Creates an empty dictionary.
        For every word in the list that was passed in:
            If it's already in the dictionary, increase it's value by one.
            Otherwise, add it to the dictionary and set it's value to one.
        Sorts freq_dict by it's values (word count) in descending order,
        then returns an ordered list of tuples.
    '''
    word_list = findall(r'\S+|\n', source_text)
    sub(r'a', 'b', 'banana')
    return word_list


def histogram_file(file_dir):
    ''' Opens the file containing text and converts it to a list of words. '''
    try:
        with open(file_dir, 'r') as file:
            text_str = file.read()
    except Exception as e:
        print(e)
        exit()
    return text_str


print(get_word_list(histogram_file('songs')))


def get_histogram(word_list, type="SD", freq_dict=None):
    if freq_dict is None:
        freq_dict = dict()
    for word in word_list:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    sorted_tuples = sorted(freq_dict.items(), key=itemgetter(1), reverse=True)
    if type == "SD":
        # sorted dictionary
        return dict(sorted_tuples)
    if type == "SL":
        # sorted 2d list
        return list(map(list, sorted_tuples))
    if type == "ST":
        # sorted list of tuples.
        return sorted_tuples


def bulk_sample(histogram, tokens, limit):
    result = []
    for _ in range(limit):
        result.append(sample_by_frequency(histogram, tokens))
    return result


def markov(word_list, word_pairs=None):
    if word_pairs is None:
        word_pairs = {}
    word_pairs['__start__'] = [word_list[0]]
    # word_pairs['__end__'] = [word_list[-1]]
    __end__ = ['__end__', word_list[-1]]

    for i in range(1, len(word_list)):
        if word_list[i-1][-1] in ['.', '?', '!', '"']:
            __end__.append(word_list[i-1])
            word_pairs['__start__'].append(word_list[i])

        if word_list[i-1] in word_pairs.keys():
            word_pairs[word_list[i-1]].append(word_list[i])
        else:
            word_pairs[word_list[i-1]] = [word_list[i]]
    for word in word_pairs.keys():
        word_pairs[word] = get_histogram(word_pairs[word], 'SL')
    word_pairs['__end__'] = __end__
    return word_pairs


def random_sentence(markov_o):
    markov = markov_o.copy()
    sentence = [sample_by_frequency(markov['__start__'], get_total_tokens(markov['__start__']))]
    try:
        while True:
            try:
                next_word = sample_by_frequency(markov[sentence[-1]], get_total_tokens(markov[sentence[-1]]))
            except:
                next_word = '__end__'
            if next_word is not '__end__':
                sentence.append(next_word)
            if next_word in markov['__end__']:
                return " ".join(sentence)
    except Exception as e:
        print("Error: "+ repr(e))
        return 0


def bulk_sentences(markov, max):
    count = 0
    results = []
    while count < max:
        rand_sentence = random_sentence(markov)
        if not rand_sentence == 0:
            results.append(rand_sentence)
            count += 1
    return results


def frequency(histogram, word):
    ''' finds the count for one word '''
    if not isinstance(histogram, dict):
        histogram = dict(histogram)
    try:
        return histogram[word]
    except:
        # Word not found
        return 0


def bulk_frequency(histogram, num):
    ''' finds all words that have the specified count '''
    print(f"All words with the count {num}:")
    count = 0
    words = []
    for word, freq in dict(histogram).items():
        if freq == num:
            count += 1
            print(f"{count}.| {word}")
            words.append(word)
    if count == 0:
        print(f"No words found.")
        return None
    return words


def unique_words(histogram):
    ''' this function is totally useless, since len() is shorter,
        but i guess this is more clear about what it's doing '''
    return len(histogram)


def get_total_tokens(histogram):
    if isinstance(histogram, dict):
        return sum(histogram.values())
    else:
        tokens = 0
        for i in range(len(histogram)):
            tokens += histogram[i][1]
        return tokens


def top_count(histogram, top_num=0):
    ''' convert dict to list of tuples (still ordered by highest to lowest frequency)
            prints the top {top_num} words and their frequencies. '''
    '''
    USE THIS TO OPTIMIZE:
    >>> d = {'a': 1, 'b': 2}
    >>> dki = d.iterkeys()
    >>> dki.next()
    'a'
    >>> dki.next()
    'b'
    >>> dki.next()
    Traceback (most recent call last):
      File "<interactive input>", line 1, in <module>
    StopIteration
    '''

    try:
        if top_num == -1:
            top_num = len(histogram)
            print(f"All {top_num} words:")
        else:
            print(f"Top {top_num} words:")
        temp_histogram = list(histogram.items())
        if 0 < top_num < len(temp_histogram):
            for i in range(top_num):
                print(f"{i+1}.| {temp_histogram[i][0]}: {frequency(histogram, temp_histogram[i][0])}")
        else:
            for i in range(len(temp_histogram)):
                print(f"{i + 1}.| {temp_histogram[i][0]}: {frequency(histogram, temp_histogram[i][0])}")
    except Exception as e:
        print(e)
        print("*** Invalid histogram ***")
        exit()


def sample_by_frequency(histogram, tokens):
    selection = random()
    floats = [0]
    if isinstance(histogram, dict):
        for word, count in histogram.items():
            floats.append((count / tokens) + floats[-1])
            if floats[-2] <= selection < floats[-1]:
                return word
    else:
        for i in range(len(histogram)):
            floats.append((histogram[i][1] / tokens) + floats[-1])
            if floats[-2] <= selection < floats[-1]:
                return histogram[i][0]

# if __name__ == '__main__':
#
#     # start = time.time()
#     mushies = Histogram('source_text', 'f')
#     print(random_sentence(mushies.markov_chain))
    # print('Mushroom e-book:')
    # print('-' * 50)
    # top_count(mushies.histogram, 5)
    # print(f"\nunique words: {unique_words(mushies.histogram)}")
    # print(f"Frequency of the word 'and': {frequency(mushies.histogram, 'and')}")
    # end = time.time()
    # print(f"Seconds: {end-start}")
    #
    # print('\n')

    # start = time.time()
    # print('How much wood could a Woodchuck chuck??:')
    # print('-' * 50)
    # woodchuck = Histogram('how much wood would a woodchuck chuck if a woodchuck could chuck wood a woodchuck would chuck as much wood as a woodchuck could chuck if a woodchuck could chuck wood')
    # print(f"\nList of Lists: {get_histogram(woodchuck.word_list, 'SL')}")
    # print(f"List of Tuples: {get_histogram(woodchuck.word_list, 'ST')}")
    # print(f"Dictionary: {woodchuck.histogram}")
    # # top_count(woodchuck.histogram, -1)
    # print(f"\nunique words: {unique_words(woodchuck.histogram)}")
    # print(f"Frequency of the word 'woodchuck': {frequency(woodchuck.histogram, 'woodchuck')}")
    # print(woodchuck.histogram)
    # print(woodchuck.markov_chain)
    # word_list = []
    # for _ in range(100000):
    #     word_list.append(sample_by_frequency(woodchuck.histogram, woodchuck.total_tokens))
    # sample_histogram = Histogram(word_list)
    # print(sample_histogram.histogram)
    # end = time.time()
    # print(f"Seconds: {end-start}")

