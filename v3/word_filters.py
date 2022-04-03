from numpy import char
from v3 import wordle_tools

def words_with_chars_at_pos(words: list[str], guesses: list[list[tuple]]) -> list[str]:
    filtered = []

    for word in words:

        matched = [False, False, False, False, False]
        valid = ["_", "_", "_", "_", "_"]

        for guess in guesses:
            for i in range(len(guess)):
                if guess[i][0] == 2:
                    valid[i] = guess[i][1]
        
        for i in range(len(valid)): 
            if valid[i] == "_":
                matched[i] = True

        for i in range(len(word)):
            if word[i] == valid[i]:
                matched[i] = True
        
        if all(matched):
            filtered.append(word)

    return filtered
    
def get_found_chars(guesses: list[list[tuple]]) -> list[int]:
    valid = ["_", "_", "_", "_", "_"]
    returned = []
    for guess in guesses:
        for i in range(len(guess)):
            if guess[i][0] == 2:
                valid[i] = guess[i][1]

    for i in range(len(valid)):
        if valid[i] != "_":
            returned.append(i)
    return returned

def words_containing_chars(words: list[str], guesses: list[list[tuple]]) -> list[str]:
    filtered = []

    not_at_pos = [set(), set(), set(), set(), set()]

    for guess in guesses:
        for i in range(len(guess)):
            if guess[i][0] == 1:
                not_at_pos[i].add(guess[i][1])

    for word in words:
        passed = True

        for i in range(len(word)):
            if word[i] in not_at_pos[i]:
                passed = False

        if passed:
            valid = 0
            needs_to_match = sum([1 if len(_set) > 0 else 0 for _set in not_at_pos])
            for i in range(len(not_at_pos)):
                can_increase = False
                for j in range(len(word)):
                    if i != j:
                        if word[j] in not_at_pos[i]:
                            can_increase = True
                if can_increase:
                    valid += 1
            if valid == needs_to_match:
                filtered.append(word)
    return filtered

def count_chars(word: str) -> dict:
    counted = {}
    for i in range(len(word)):
        if word[i] not in counted:
            counted[word[i]] = 1
        else:
            counted[word[i]] += 1
    return counted


def words_not_containing_chars(words: list[str], guesses: list[list[tuple]]) -> list[str]:
    correct = []

    invalid_charset = set()

    can_have = {}
    cant_have = {}

    for guess in guesses:
        for i in range(len(guess)):
            if guess[i][0] == 0:
                invalid_charset.add(guess[i][1])
                if guess[i][1] not in cant_have:
                    cant_have[guess[i][1]] = [i]
                else:
                    cant_have[guess[i][1]] += [i]
            elif guess[i][0] == 2 or guess[i][0] == 1:
                if guess[i][1] not in can_have:
                    can_have[guess[i][1]] = [i]
                else:
                    can_have[guess[i][1]] += [i]

    for word in words:
        passed_duplicates_tests = True

        for i in range(len(word)):
            if word[i] in can_have and word[i] in cant_have:
                if i in cant_have[word[i]]:
                    passed_duplicates_tests = False
        if passed_duplicates_tests:
            valid = True
            for i in range(len(word)):
                if word[i] in cant_have and i in cant_have[word[i]]:
                    valid = False
            if valid:
                correct.append(word)
    return correct

def master_filter(words: list[str], guesses: list[list[tuple]]) -> list[str]:
    wordlist = []

    wordlist = words_not_containing_chars(words, guesses)
    wordlist = words_containing_chars(wordlist, guesses)
    wordlist = words_with_chars_at_pos(wordlist, guesses)

    final = []

    for guess in guesses:
        word = "".join(wordle_tools.get_word_from_results(guess))
        for _word in wordlist:
            if _word != word and _word not in final:
                final.append(_word)
    return final