import v3.wordle_tools as wordle_tools
import v3.word_filters as word_filters

def probability(word: str, x: list[str]):
    patterns = {}
    probability = {}

    for _word in x:
        pattern = wordle_tools.get_pattern_from_results(wordle_tools.calculate_pattern_from_guess(word, _word))
        if tuple(pattern) not in patterns:
            patterns[tuple(pattern)] = 1
        else:
            patterns[tuple(pattern)] += 1
    
    for pattern in patterns:
        probability[tuple(pattern)] = patterns[tuple(pattern)] / len(x)
    
    return probability