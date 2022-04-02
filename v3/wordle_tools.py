with open("./data/words.txt") as f:
    WORDS = f.read().split("\n")

CHARS = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

"""with open("./frequency-data.txt") as f:
    FREQ_DATA = {}
    lines = f.read().split("\n")
    for i in range(len(lines)):
        split = lines[i].split(",")
        FREQ_DATA[split[1]] = {}
        FREQ_DATA[split[1]]["count"] = int(split[2])
        FREQ_DATA[split[1]]["frequency"] = float(split[3])"""


def get_positioned_correctly_chars(word: str, correct_word: str) -> list[str]:
    correct = ["_", "_", "_", "_", "_"]
    for i in range(len(word)):
        if word[i] == correct_word[i]:
            correct[i] = word[i]
    return correct

def get_guessed_correctly_chars(word: str, correct_word: str) -> list[str]:
    correct = ["_", "_", "_", "_", "_"]
    char_count = {}
    already_counted = {}

    for c in correct_word:
        if c not in char_count:
            char_count[c] = 1
        else:
            char_count[c] += 1

    for i in range(len(word)):
        if word[i] != correct_word[i]:
            if word[i] in already_counted and word[i] in char_count and char_count[word[i]] > already_counted[word[i]]:
                already_counted[word[i]] += 1
                correct[i] = word[i]
            elif word[i] not in already_counted and word[i] in char_count:
                already_counted[word[i]] = 1
                correct[i] = word[i]

    return correct

def get_incorrect_chars(word: str, correct_word: str) -> list[str]:
    incorrect = ["_", "_", "_", "_", "_"]

    char_count = {}
    already_counted = {}

    for c in word:
        if c not in char_count:
            char_count[c] = 1
        else:
            char_count[c] += 1

    for i in range(len(word)):
        if word[i] not in correct_word:
            incorrect[i] = word[i]
        else:
            if word[i] in char_count and word[i] not in already_counted:
                already_counted[word[i]] = 1
            elif char_count[word[i]] > already_counted[word[i]]:
                already_counted[word[i]] += 1
                incorrect[i] = word[i]
    return incorrect

def calculate_pattern_from_guess(word: str, correct_word: str) -> list[str]:
    pattern = [(), (), (), (), ()]

    pos_correct = get_positioned_correctly_chars(word, correct_word)
    pos_incorrect = get_guessed_correctly_chars(word, correct_word)
    not_in = get_incorrect_chars(word, correct_word)

    letter_counts = {}

    for i in range(len(correct_word)):
        if correct_word[i] not in letter_counts:
            letter_counts[correct_word[i]] = 1
        else:
            letter_counts[correct_word[i]] += 1

    fulfilled = {}

    already_executed = set()

    for i in range(len(word)):
        if pos_correct[i] != "_":
            if pos_correct[i] in fulfilled:
                fulfilled[pos_correct[i]] += 1
            else:
                fulfilled[pos_correct[i]] = 1
            pattern[i] = (2, pos_correct[i])
            already_executed.add(i)
            
    for i in range(len(word)):
        if pos_incorrect[i] != "_" and i not in already_executed:
            if pos_incorrect[i] in fulfilled:
                if fulfilled[pos_incorrect[i]] == letter_counts[pos_incorrect[i]]:
                    pattern[i] = (0, pos_incorrect[i])
                else:
                    fulfilled[pos_incorrect[i]] += 1
                    pattern[i] = (1, pos_incorrect[i])
            else:
                fulfilled[pos_incorrect[i]] = 1
                pattern[i] = (1, pos_incorrect[i])

    for i in range(len(word)):
        if not_in[i] != "_" and i not in already_executed:
            pattern[i] = (0, not_in[i])
    
    return pattern

def get_pattern_from_results(results: list[tuple]):
    return [c[0] for c in results]

def get_word_from_results(results: list[tuple]):
    return [c[1] for c in results]
