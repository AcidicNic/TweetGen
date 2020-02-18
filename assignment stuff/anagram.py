'''
    python anagram.py <word>
    --> [any anagrams for the word.]
'''
from sys import argv
from re import sub


def setup_dict():
    with open("/usr/share/dict/words", 'r') as dict_file:
        dict_list = dict_file.read().splitlines()
    return dict_list


def sort_word(word):
    ''' sorts str word alphabelically '''
    return''.join(sorted(word.lower()))


def sorted_words(word_list):
    ''' for every word in word_list, sort the word's characters alphabelically, return new list '''
    result = []
    for word in word_list:
        result.append(sort_word(word))
    return result


def find_anagrams(word, word_list, sorted_words):
    ''' search through every word in sorted_words to find  '''
    anagrams = []
    sorted_word = sort_word(word)
    for i in range(len(sorted_words)):
        if sorted_words[i] == sorted_word and not word.lower() == word_list[i].lower():
            anagrams.append(word_list[i])
    return anagrams


if __name__ == '__main__':
    if len(argv) > 1:
        word_list = setup_dict()
        sorted_words = sorted_words(word_list)
        anagrams = find_anagrams(argv[1], word_list, sorted_words)
        if len(anagrams) > 0:
            print(f"Anagrams for {argv[1]}:")
            for word in anagrams:
                print(f" * {word}")
        else:
            print(f"No anagrams found for {argv[1]}")
    else:
        print("enter a word, I'll find an anagram for it")
