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
    second_filtered = []

    found_chars = get_found_chars(guesses)

    not_at_pos = [set(), set(), set(), set(), set()]
    ones_count = 0
    precheck = set()

    for i in range(len(guesses[len(guesses) - 1])):
        if guesses[len(guesses) - 1][i][0] == 1:
            not_at_pos[i].add(guesses[len(guesses) - 1][i][1])
            if guesses[len(guesses) - 1][i][1] not in precheck:
                ones_count += 1
                precheck.add(guesses[len(guesses) - 1][i][1])

    for i in range(len(found_chars)):
        if found_chars[i] != "_":
            not_at_pos[i] = set()

    for word in words:
        matched = [False, False, False, False, False]

        for i in range(len(word)):
            if len(not_at_pos[i]):
                matched[i] = True
            elif word[i] not in not_at_pos[i]:
                matched[i] = True
        if all(matched):
            filtered.append(word)
    
    for word in filtered:
        holder = 0
        checked = set()
        for i in range(len(not_at_pos)):
            mset = set()
            for j in range(len(not_at_pos)):
                 if j != i and j not in found_chars:
                     mset = mset.union(*not_at_pos[j])
            
            if word[i] in mset and word[i] not in checked:
                holder += 1
                checked.add(word[i])
        if holder == ones_count:
            second_filtered.append(word)
    
    return second_filtered

def words_not_containing_chars(words: list[str], guesses: list[list[tuple]]) -> list[str]:
    correct = []

    letter_count = {}
    checked = set()

    invalid_charset = set()
    for guess in guesses:
        for i in range(len(guess)):
            if guess[i][0] == 0:
                invalid_charset.add(guess[i][1])
            elif guess[i][0] == 1 or guess[i][0] == 2:
                if guess[i][1] not in letter_count:
                    pass
    for word in words:
        valid = True
        for c in invalid_charset:
            if c in word:
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
            if _word != word:
                final.append(_word)

    return final