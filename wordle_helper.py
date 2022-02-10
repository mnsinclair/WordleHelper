from enum import Enum, auto

import numpy as np
import pandas as pd

class color(Enum):
    red = auto()
    orange = auto()
    green = auto()
    
def get_word_scores(word_set: set, char_scores: dict) -> dict:
    """This function creates a dictionary with english words as keys numeric 'word scores' as values.
    
    This score is derived from how 'common' the comprising chars of the word are, and discourages repeating chars.
    The word with the  highest score will be used as the next guess in the game.
    
    Python dictionaries preserve the order by which key-value pairs are inserted.
    An iterable of (word, score) pairs is created, which is then inserted into the dictionary in decreasing score order.
    This means we have the best of both worlds with the data strtucture:
    
        - A sorted collection, which means we can easily select the word with the best score to be our guess each round
        - A hash-map structure with constant-time deletion of key-value pairs 
          (this happens VERY frequently as we eliminate words).
    
    Args:
        - word_set: a set of the english words to be scored
        - char_scores: a dictionary with alphabetical characters as keys, and corresponding 'character scores' as values.
        
    Returns:
        - word_scores: a dictionary with english words as keys numeric 'word scores' as values, 
                       inserted in order of descending score value.   
    """
    
    score_word_pairs = list()
    
    for word in word_set:    
        score = 0
        used_chars = set()
        
        for char in word:
            # A character should only contribute to a word score if:
                #  The character has a score in char_scores
                #  AND
                #  The character has not been used in this word before (we don't want to encourage repeating chars)
                
            if char in char_scores and char not in used_chars:
                score += char_scores[char]
                used_chars.add(char)
                
        score_word_pairs.append((word, score))
    
    # Generate a diction with word : score pairs added in descending score order.
    word_scores = {word : round(score,2) for word, score in sorted(score_word_pairs, key = lambda x: x[1], reverse = True)}
        
    return word_scores

def prune_word_scores(char: str, pos: int, color: color, word_scores: dict) -> None:
    """This function reduces the wordle search space using information about the color yielded by a char at given position
    
    Note this function does not have a return value - it removes key-value pairs from the word_scores collection.
    
    Args:
        - char: a single character string
        - pos: the index of char within the guess
        - color: A color object indicating the color yielded by guessing 'char' in position 'pos' (red, orange or green)
    """
    to_remove = set()
    
    for word in word_scores:
        # If the color is red, the char is not in the word. 
        if color == color.red:
            # Any word with the char should be removed.
            if char in word:
                to_remove.add(word)
        # If the color is orange, the char is in the word, but not at the current position.
        elif color == color.orange:
            # Any word with the char in the current position, or without the char in any position should be removed. 
            if char == word[pos] or char not in word:
                to_remove.add(word)
        # If the color is green, the char is in the correct position.
        else: # color is green
            # Any word with a different char in this position should be removed.
            if char != word[pos]:
                to_remove.add(word)
    
    # Remove all the words that meet the above conditions.
    for word in to_remove:
        del word_scores[word]
        
def make_guess(guess_word: str, target_word: str) -> np.array:
    """This function compares a guess word with a target word, and returns an array of 'color' objects in the wordle style.
    
    Args:
        - guess_word: 5-character guess string
        - target_word: 5-character target string
    
    Returns:
        - result: np.array of 5 'color' objects.
    """
    assert len(guess_word) == len(target_word), "Guess word and target word must be the same length"
    
    # intialise a 1D numpy array with 5 values to hold the guess result   
    result = np.empty(len(guess_word), dtype = object)
    
    for i, (guess_char, target_char) in enumerate(zip(guess_word.lower(), target_word.lower())):
        if guess_char == target_char: # green if chars match
            char_color = color.green
        elif guess_char in target_word: # orange if char is in word (but not position match)
            char_color = color.orange
        else:
            char_color = color.red # red if above conditions not met.
        
        result[i] = char_color
        
    return result    

def get_next_guess(word_scores: dict) -> str:
    """
    This function returns a string representing the next guess the player should make in the wordle game.
    
    Args:
        - word_scores: dictionary of english word : numeric_score pairs.
        
    Returns:
        - next_guess: string representing the next guess the player should make in the wordle game.
    """
    
    # Creating an iterable just to grab the first element seems wasteful, 
    # but I'm not sure how to do it any other way. Suggestions welcome!
    
    next_guess = next(iter(word_scores))
    
    return next_guess

def check_target_match(guess_result: np.array) -> bool:
    """This function checks whether all colors within a guess result are green.
    
    This is useful in checking whether the word has been found.
    
    Args: 
        - guess_result: a np.array object with the result of a guess.
    Returns:
        - is_match: a boolean value signifying whether all members of guess_result are 'green'
    """
    
    is_match = (guess_result == color.green).all()
    
    return is_match