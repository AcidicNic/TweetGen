from operator import itemgetter
from random import random
from re import sub
from sys import exit
import time
from prettytable import PrettyTable
from statistics import mean
import source_text


''' !!!
make different markov and word counting fxn to include whitespace and recreate a whole song, with the syntax and everything.
!!! '''


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
    if isinstance(source_text, str):
        word_list = source_text.split()
    elif isinstance(source_text, list):
        word_list = source_text
    else:
        print("*** invalid source text ***")
        return None
    # r = re.compile(r"[^a-zA-Z0-9-,.?!()]+")

    for i in reversed(range(len(word_list))):
        # remove any character that isn't a-z or 0-9 at the beginning or end of each string
        word_list[i] = sub(r'[()"[\]{}]', '', word_list[i])
        # r.sub("", word_list[i])
        # remove from word list if it's an empty string.
        if word_list[i] == '':
            word_list.pop(i)
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


def markov(word_list, word_pairs=None):
    """ This is the data structure we need to actually generate random sentences!
        each word is added to a dictionary
        '__start__' and '__end__' are strings I use to tell my program where it's okay to start and end sentences!
            You'll notice that the value for '__end__' is a list, not a nested list of word & count pairs.
            This list contains words that are at the end of their sentence


        {
            '__start__': [[<str: next_word>, <int: count>], [<str: next_word>, <int: count>]],
            word: [[word, count], [word, count], [word, count], [word, count]],
            word: [['__end__', 1], [word, count]],
            '__end__': [word, word, word]
        }
    """
    if word_pairs is None:
        word_pairs = {}
    word_pairs['__start__'] = [word_list[0]]
    word_pairs[word_list[-1]] = ['__end__']
    __end__ = [word_list[-1]]

    for i in range(1, len(word_list)):
        word = word_list[i-1]
        next_word = word_list[i]
        if word[-1] in ['.', '?', '!', '"']:
            __end__.append(word_list[i-1])
            word_pairs['__start__'].append(next_word)
            next_word = '__end__'

        if word in word_pairs.keys():
            word_pairs[word].append(next_word)
        else:
            word_pairs[word] = [next_word]
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
            else:
                return " ".join(sentence)
    except Exception as e:
        print("Error: " + repr(e))
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


def find_frequency(histogram, num):
    ''' finds all words that have the specified count '''
    count = 0
    words = []
    for word, freq in dict(histogram).items():
        if freq == num:
            count += 1
            words.append(word)
    if count == 0:
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


def top_count(histogram, top_num=5):
    ''' convert dict to list of tuples (still ordered by highest to lowest frequency)
        dictogram: histogram
        returns a prettytable the top {top_num} words and their frequencies. '''
    t = PrettyTable()
    if 0 > top_num or len(histogram) <= top_num:
        top_num = len(histogram)
        t.title = f'All {top_num} Words'
    else:
        t.title = f'Top {top_num} Words'
    t.field_names = ['--', 'Word', 'n']
    t.align['Word'] = 'l'
    i = 1
    for k, v in histogram.items():
        t.add_row([f'{i}.', k, v])
        i += 1
        if i > top_num:
            return t


def sample_by_frequency(histogram, tokens, num=1):
    words = []
    floats = [0]
    if num > 1:
        selections = []
        for i in range(num):
            selections.append(random())
        selections.sort(reverse=True)
        if isinstance(histogram, dict):
            for word, count in histogram.items():
                floats.append((count / tokens) + floats[-1])
                while floats[-2] <= selections[-1] < floats[-1]:
                    words.append(word)
                    selections.pop()
                    if len(selections) == 0:
                        return words
        else:
            for i in range(len(histogram)):
                floats.append((histogram[i][1] / tokens) + floats[-1])
                while floats[-2] <= selections[-1] < floats[-1]:
                    words.append(histogram[i][0])
                    selections.pop()
                    if len(selections) == 0:
                        return words
    else:
        selection = random()
        if isinstance(histogram, dict):
            for word, count in histogram.items():
                floats.append((count / tokens) + floats[-1])
                if floats[-2] <= selection < floats[-1]:
                    return word
        else:
            for i in range(len(histogram)):
                floats.append((histogram[i][1] / tokens) + floats[-1])
                while floats[-2] <= selection < floats[-1]:
                    return histogram[i][0]


''' Test Helpers '''


def print_title(title):
    """ Prints pretty titles """
    print(f'{title}:\n-{"-" * len(title)}')


def compare_hists(actual, a_tokens, s_tokens=100000, only_stats=False):
    """ Gives you some fun stats to test sample_by_frequency()

        Parameters:
            actual (dict histogram): the histogram you want to randomly sample from.
            a_tokens (int): total tokens of the given histogram
            s_tokens (int): # of words you'd like to sample.
            only_stats (bool): If true it will not return the list of each word with it's percent error, only the
                               total sampled (s_tokens), the histogram's total tokens (a_tokens), and the avg % error.

        Returns:
            str: pretty table of stats.

    """
    word_list = sample_by_frequency(actual, a_tokens, s_tokens)
    sample = Histogram(word_list).histogram
    st_to_at = s_tokens/a_tokens

    percent_errs = []
    if only_stats:
        for k, v in sample.items():
            exact = actual[k] * st_to_at
            percent_errs.append((v - exact) / exact * 100)
        stats = PrettyTable(['Unique Words in Source', len(actual)], hrules=True)
        stats.title = f"{s_tokens} words sampled by freq"
        stats.add_row(['Avg % Error', f"{mean(percent_errs):,.2f}%"])
        return stats
    else:
        t = PrettyTable(['Word', 'Exact', 'Sampled', "% Error"])
        t.title = f"{s_tokens} words sampled by freq"
        t.align['% Error'] = 'r'
        for k, v in sample.items():
            exact = actual[k] * st_to_at
            percent_err = (v - exact) / exact * 100
            t.add_row([k, int(exact), v, f"{percent_err:,.2f}%"])
            percent_errs.append(percent_err)
        stats = PrettyTable(['Unique Words in Source', len(actual)], hrules=True)
        stats.add_row(['Avg % Error', f"{mean(percent_errs):,.2f}%"])
        return f"{t}\n{stats}"


''' Tests / Demonstrations '''


def cuco_test():
    start = time.time()
    cuco = Histogram(source_text.cuco)
    print_title('Cuco Songs')
    print(f"unique words: {unique_words(cuco.histogram)}")

    print(top_count(cuco.histogram, 3))
    print(f"Frequency of the word 'you': {frequency(cuco.histogram, 'you')}")
    print(f"Frequency of the word 'wtf': {frequency(cuco.histogram, 'wtf')}")
    print(f"\nAll words with count 7: {', '.join(find_frequency(cuco.histogram, 7))}")
    print(f"Frequency of the word 'like': {frequency(cuco.histogram, 'like')}")

    print(compare_hists(cuco.histogram, cuco.total_tokens, 100000, True))

    print('\n5 Random "Sentences"!')
    for sentence in bulk_sentences(cuco.markov_chain, 5):
        print(f"\t{sentence}")

    print(f"Cuco Benchmark: {time.time() - start:,.3f} seconds")


def woodchuck_test():
    start = time.time()
    woodchuck = Histogram('How much wood would a woodchuck chuck if a woodchuck could chuck wood? A woodchuck would '
                          'chuck as much wood as a woodchuck could chuck if a woodchuck could chuck wood.')
    print_title("How much wood could a Woodchuck chuck?")
    print(f"unique words: {unique_words(woodchuck.histogram)}")

    print("Histogram Types:")
    print(f"List of Lists: {get_histogram(woodchuck.word_list, 'SL')}")
    print(f"List of Tuples: {get_histogram(woodchuck.word_list, 'ST')}")
    print(f"Dictionary: {woodchuck.histogram}")

    print(f"\nMarkov Chain: {woodchuck.markov_chain}")

    print(top_count(woodchuck.histogram))
    # print(f"Frequency of the word 'woodchuck': {frequency(woodchuck.histogram, 'woodchuck')}")

    # print(compare_hists(woodchuck.histogram, woodchuck.total_tokens))

    print(f"Woodchuck Benchmark: {time.time() - start:,.2f} seconds")


def fish_test():
    start = time.time()
    fish_txt = 'One Fish Two Fish Red Fish Blue Fish'
    print_title(fish_txt)
    fish = Histogram(fish_txt.lower())

    # print("Histogram Types:")
    # print(f"List of Lists: {get_histogram(fish.word_list, 'SL')}")
    # print(f"List of Tuples: {get_histogram(fish.word_list, 'ST')}")
    print(f"Dictionary: {fish.histogram}")

    # print(top_count(fish.histogram, -1))
    # print(f"Frequency of the word 'fish': {frequency(fish.histogram, 'fish')}")
    # print(f"Frequency of the word 'the': {frequency(fish.histogram, 'the')}")
    # print(f"Markov Chain:   {fish.markov_chain}")

    print(compare_hists(fish.histogram, fish.total_tokens))

    print(f"Fish Benchmark: {time.time() - start:,.2f} seconds")


if __name__ == '__main__':
    fish_test()
    print('\n')
    woodchuck_test()
    print('\n')
    cuco_test()


