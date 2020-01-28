'''
    python dictionary_words.py [optional: number of random words you want]
'''
from sys import argv
from random import randrange


def setup_dict():
    with open("/usr/share/dict/words", 'r') as dict_file:
        dict_list = dict_file.read().splitlines()
    return dict_list


def random_words(word_num=1):
    dict_list = setup_dict()
    for _ in range(int(word_num)):
        rand_index = randrange(len(dict_list))
        print(dict_list[rand_index])


if __name__ == '__main__':
    if len(argv) == 2:
        random_words(argv[1])
    else:
        random_words()
