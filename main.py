import argparse


with open('wordlist.txt', 'r') as file:
    wordlist = file.read()
    wordlist = wordlist.split()

letter_points = {  # Create a dictionary to store the points for each letter
    'a': 1,     'b': 3,     'c': 3,
    'd': 2,     'e': 1,     'f': 4,
    'g': 2,     'h': 4,     'i': 1,
    'j': 8,     'k': 5,     'l': 2,
    'm': 3,     'n': 1,     'o': 1,
    'p': 3,     'q': 10,    'r': 1,
    's': 1,     't': 1,     'u': 1,
    'v': 4,     'w': 4,     'x': 8,
    'y': 4,     'z': 10,    '_': 0
}

# Checks if a word can be constructed with the given letters and returns the amount of points if it can
def word_can_be_constructed(letters, word):
    points = 0
    blanks = letters.count('_')
    missing_letters = 0
    available_letters = letters.copy()

    for char in word:
        if char in available_letters:
            available_letters.remove(char)
            points += letter_points[char]
        else:
            missing_letters += 1
            if missing_letters > blanks:
                break

    return points if blanks >= missing_letters else None


# Goes through every word in the wordlist and returns the list of possible words and their respective points
def get_words_for_chars(letters):
    list = {}

    for word in wordlist:
        points = word_can_be_constructed(letters, word)
        if points != None:
            list[word] = points
            
    return list


def get_words_with_pattern(letters, pattern):
    list = {}
    available_letters = letters.copy()

    for char in pattern:
        available_letters.append(char)

    for word in wordlist:
        if pattern in word and word != pattern:
            points = word_can_be_constructed(available_letters, word)
            if points != None:
                list[word] = points
            
    return list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-letters', required=True)
    parser.add_argument('-words', nargs='+', required=False)
    parser.add_argument('-start', required=False)
    parser.add_argument('-end', required=False)
    args = parser.parse_args()

    my_letters = args.letters
    my_letters = my_letters.strip()  # Remove any whitespace
    my_letters = [char for char in my_letters]  # Make a list containing each letter

    ready_words = args.words
    starts_with = args.start
    ends_with = args.end

    possible_words = {}  # Dictionary to store all possible words and their points

    possible_words.update(get_words_for_chars(my_letters))

    if ready_words != None:
        for word in ready_words:
            for char in word:
                my_letters_plus = my_letters.copy()
                my_letters_plus.append(char)
                possible_words.update(get_words_for_chars(my_letters_plus))
            
            possible_words.update(get_words_with_pattern(my_letters, word))

    words_to_remove = []

    for word in possible_words:
        if starts_with != None and not word.startswith(starts_with):
            words_to_remove.append(word)
        if ends_with != None and not word.endswith(ends_with):
            words_to_remove.append(word)

    for word in words_to_remove:
        possible_words.pop(word, None)

    possible_words = sorted(possible_words.items(), key=lambda x: x[1], reverse=False)  # Sort the words based on points given

    for word, points in possible_words[-100:]:  # Only list the top 100 words
        print(f'{word}: {points}')
    

if __name__ == '__main__':
    main()
