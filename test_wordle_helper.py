import unittest
from wordle_helper import *

import numpy as np

class TestWordleHelper(unittest.TestCase):

    def test_get_word_scores(self):
        word_set = {"aaaaa", "aaaab", "aaabc", "acbac"}
        char_scores = {"a" : 1, "b" : 2, "c" : 3}
        
        word_scores = get_word_scores(word_set, char_scores)
        
        # Check that repeated characters are only counted once.
        self.assertEqual(word_scores["aaaaa"], char_scores["a"])
        
        # Check that score is the sum of the two characters appearing in the string.
        self.assertEqual(word_scores["aaaab"], char_scores["a"] + char_scores["b"])
        
        # Check that the score is the sum of the three characters appearing in the string.
        self.assertEqual(word_scores["aaabc"], char_scores["a"] + char_scores["b"] + char_scores["c"])
        
        # Check that the score is position-agnostic
        self.assertEqual(word_scores["acbac"], char_scores["a"] + char_scores["b"] + char_scores["c"])
        
        # Check that the key-value pairs are inserted in the dictionary in descending numerical order.
        self.assertEqual([value for value in word_scores.values()], [6,6,3,1])

    def test_prune_word_scores(self):
        word_scores_template = {"R2D": 2, "C3P" : 0, "BB-" : 8, "R5D" : 4, "IG-" : 11}
        
        # Test that the pruning removes all instances that contain "char" at any position when the color is "red".
        word_scores = word_scores_template.copy()
        red_pruned = {"C3P" : 0, "BB-" : 8, "IG-" : 11}
        prune_word_scores(char = "R", pos = 0, color = color.red, word_scores = word_scores)
        self.assertEqual(word_scores, red_pruned)
        
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "R", pos = 1, color = color.red, word_scores = word_scores)
        self.assertEqual(word_scores, red_pruned)
        
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "R", pos = 2, color = color.red, word_scores = word_scores)
        self.assertEqual(word_scores, red_pruned)
        
        # Test that the pruning removes all instances that do not contain "char" at any OTHER position when color is "orange".
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "B", pos = 2, color = color.orange, word_scores = word_scores)
        self.assertEqual(word_scores, {"BB-" : 8})
        
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "D", pos = 0, color = color.orange, word_scores = word_scores)
        self.assertEqual(word_scores, {"R2D": 2, "R5D" : 4})
        
        # Test that the pruning removes all instances that contain "char" at "pos" when color is "orange".
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "B", pos = 1, color = color.orange, word_scores = word_scores)
        self.assertEqual(word_scores, {})
        
        # Test that the pruning removes all instances that do not contain "char" at "pos" when color is "green"
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "R", pos = 0, color = color.green, word_scores = word_scores)
        self.assertEqual(word_scores, {"R2D": 2, "R5D" : 4})
        
        word_scores = word_scores_template.copy()
        prune_word_scores(char = "-", pos = 2, color = color.green, word_scores = word_scores)
        self.assertEqual(word_scores, {"BB-" : 8, "IG-" : 11})        


    def test_make_guess(self):
        target = "MasterYoda"
        guess = "MasterLuke"
        
        def compare_result(returned_colors, expected_colors):
            for returned_color, expected_color in zip(returned_colors, expected_colors):
                self.assertEqual(returned_color, expected_color)
        
        returned = make_guess(guess_word = guess, target_word = target)
        expected = [color.green for _ in range(6)] + [color.red for _ in range(3)] + [color.orange]
        compare_result(returned, expected)
        
        target = "DarthVader"
        guess = "SithJarJar" # Check out the fan-theory...
        
        returned = make_guess(guess_word = guess, target_word = target)
        expected = [color.red, color.red, color.orange, color.orange, color.red, color.orange, color.orange, color.red, color.orange, color.green]

    def test_get_next_guess(self):
        strings = ["Just another...", "...happy landing", "There's always...", "...a bigger fish", "I hate sand...", "...it's coarse, and irritating!", "Like a bantha...", "...Yes?!", "This is...", "...the way"]
        
        dictionary = {string : i for i, string in enumerate(strings)}
        
        self.assertEqual(get_next_guess(dictionary), "Just another...")
        
        dictionary = {string : i for i, string in enumerate(sorted(strings))}
        self.assertEqual(get_next_guess(dictionary), "...Yes?!")
        
        dictionary = {string : i for i, string in enumerate(sorted(strings, reverse = True))}
        self.assertEqual(get_next_guess(dictionary), "This is...")
        
    
    def test_check_target_match(self):
        # check true if any number of 'green' in array
        for i in range(10):
            self.assertTrue(check_target_match(np.array([color.green for _ in range(i)])))
        
        # check false if orange in array
        self.assertFalse(check_target_match(np.array([color.orange])))
        # check false if red in array
        self.assertFalse(check_target_match(np.array([color.red])))
        
        # check false if both green and red in array
        self.assertFalse(check_target_match(np.array([color.green, color.orange])))
        # check false if both green and red in array
        self.assertFalse(check_target_match(np.array([color.green, color.red])))
        # check false if both orange and red in array
        self.assertFalse(check_target_match(np.array([color.orange, color.red])))
        
        # check false if both orange and red and green in array
        self.assertFalse(check_target_match(np.array([color.orange, color.red, color.green])))

if __name__ == "__main__":
    unittest.main()