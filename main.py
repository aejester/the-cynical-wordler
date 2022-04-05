#!/usr/bin/env python3.9

from util.env_reader import read_env
from v3 import probability
from v3 import visual_utilities
from v3 import wordle_tools
from v3 import word_filters

import math
import tweepy
import random
import datetime
import time

def run():
    env = read_env()

    with open("./data/valid_words.txt", "r") as f_v_w:
        valid_words = f_v_w.read().split("\n")

    with open("./last_solved_wordle.txt", "r") as l_s:
        last_solved = int(l_s.read().strip())

    try:
        word = valid_words[last_solved + 1]
    except IndexError:
        exit()

    with open("./data/valid_words.txt", "r") as v_w:
        valid_words = v_w.read().split("\n")
    
    guesses = []
    initial_guess = "tares"
    guesses.append(wordle_tools.calculate_pattern_from_guess(initial_guess, word))

    words = word_filters.master_filter(wordle_tools.WORDS, guesses)

    while sum(wordle_tools.get_pattern_from_results(guesses[len(guesses)-1])) != 10 and len(guesses) < 6:
        largest_words = []

        for i in range(len(words)):
            px = probability.probability(words[i], words)

            summation = 0

            for key in px:
                summation += px[key] * math.log2(1/px[key])

            largest_words.append((words[i], summation))

        sorted_largest_words = sorted(largest_words, key=lambda p_word: p_word[1])
        
        try:
            guesses.append(wordle_tools.calculate_pattern_from_guess(sorted_largest_words[len(sorted_largest_words) - 1][0], word))
        except IndexError:
            break

        words = word_filters.master_filter(words, guesses)

    wordle = "Wordle "+str(last_solved + 1)+" "+str(len(guesses) if sum(wordle_tools.get_pattern_from_results(guesses[len(guesses)-1])) != 10 else "X")+"/6*\n\n"+visual_utilities.build_wordle_grid(guesses)
    line = ""

    with open("./data/solved_lines.txt", "r") as s_l:
        solved_lines = s_l.read().split("\n")

    with open("./data/didnt_solve_lines.txt", "r") as d_s_l:
        didnt_solve_lines = d_s_l.read().split("\n")

    if "X" in wordle or sum(wordle_tools.get_pattern_from_results(guesses[len(guesses)-1])) != 10:
        line = didnt_solve_lines[random.randint(0, len(didnt_solve_lines) - 1)]
    else:
        line = solved_lines[random.randint(0, len(solved_lines) - 1)]

    tweet = line+"\n"+wordle

    print(tweet)

    auth = tweepy.OAuthHandler(env["api_key"], env["api_key_secret"])
    auth.set_access_token(env["access_token"], env["access_token_secret"])
    api = tweepy.API(auth)

    api.update_status(status=tweet)

    print("\n\n------------------------\n\nNOT_TWEETED="+word+" (for verification)")
    print(guesses)

    f = open("./last_solved_wordle.txt", "w")
    f.write(str(last_solved + 1))
    f.close()

    return "".join(wordle_tools.get_word_from_results(guesses[len(guesses) - 1])) == word

hour = int(datetime.datetime.now().strftime("%H"))
already_tweeted = False
while True:
    print(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")+", already_tweeted="+str(already_tweeted)+", hour="+str(hour))
    if hour == 0 and already_tweeted == False:
        result = run()
        hour = int(datetime.datetime.now().strftime("%H"))
        already_tweeted = True
    elif hour != int(datetime.datetime.now().strftime("%H")) and hour == 23:
        already_tweeted = False

    hour = int(datetime.datetime.now().strftime("%H"))

    time.sleep(60)