from IPython import get_ipython
get_ipython().system('pip install english-words')
from english_words import english_words_lower_alpha_set

import wordle_helper

if __name__ == "__main__":
  
    wordle_words = {word for word in english_words_lower_alpha_set if len(word) == 5}
    
    # Read in the proportion of char occurance. https://www.lexico.com/explore/which-letters-are-used-most
    freq = pd.read_csv('letter_frequency.csv')

    # Strip the percentage sign from the "Percentage" column, and cast to floating point number.
    freq.Percentage = pd.Series([float(val.strip("%")) for val in freq.Percentage])

    # Convert the pandas dataframe into a frequency dictionary. Keys are the chars, values are the proportions.
    char_scores = dict()
    for _, (char, percentage) in freq.iterrows():
        char_scores[char.lower()] = percentage

    word_scores = get_word_scores(wordle_words, char_scores)

    while True:
        # Get next 'best guess'
        guess_word = get_next_guess(word_scores)

        print("Best next guess is:", guess_word.upper())

        # Make the guess, and get the resulting colors 
        guess_result = np.zeros(5, dtype = object)
        for i in range(5):
            color_input = None
            while color_input not in {"r", "o", "g"}:
                color_input = input(f"\'{guess_word[i].upper()}\' in position {i + 1} was (r)ed, (o)range, (g)reen:    ")
            if color_input == "r":
                guess_result[i] = color.red
            elif color_input == "o":
                guess_result[i] = color.orange
            else:
                guess_result[i] = color.green
 
        # Check if the guess is a full match (all green)
        if check_target_match(guess_result):    
            print(f"Woohoo! the final word was f{guess_word}")
            break
        else:
            for i, (color, guess_char) in enumerate(zip(guess_result, guess_word)):
                prune_word_scores(char = guess_char, pos = i, color = color, word_scores = word_scores)

