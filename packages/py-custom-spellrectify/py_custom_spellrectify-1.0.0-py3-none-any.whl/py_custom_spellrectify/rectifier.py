##################################################
## Author: Vimal Dharmalingam
## License: MIT Licence
## Maintainer: Vimal Dharmalingam, Maurya Allimuthu
## Email: vimal Dharmalingam <vimald8959@gmail.com>
##################################################


from difflib import SequenceMatcher
import numpy as np

class Error(Exception):
   """Base class for other exceptions"""
   pass


class ZeroInput(Error):

    def __init__(self):
        pass

class InvalidWord(Error):

    def __init__(self):
        pass


class WordCorrection:
    custom_list = []
    exclude_list =[]

    def __init__(self):
        pass

    def custom_list(self):
        return self.custom_list

    def remove(self, words=[]):
        try:
            if len(words) == 0:
                raise ZeroInput()
            else:
                final_custom_list = list(set(self.custom_list) - set(words))
                self.custom_list = final_custom_list

        except ZeroInput:
            print("Please give more than one word(s)")

    def exclude(self, words=[]):
        try:
            if len(words) == 0:
                raise ZeroInput()
            else:
                self.exclude_list = words

        except ZeroInput:
            print("Please give more than one word(s)")



    def load(self, file=None, input_words=[]):
        if file == None:
            # input runtime
            try:
                if len(input_words) == 0:
                    raise ZeroInput()
                self.custom_list = input_words
            except ZeroInput:
                print("Please give more than one word(s)")
        else:
            # input via file text
            pass

    def correct(self, input=None, threshold=0):
        try:
            if input == None:
                raise InvalidWord()
            if len(input) > 0:
                final_list = list(set(self.custom_list) - set(self.exclude_list))
                # print(final_list)
                output = [SequenceMatcher(None, input.lower(), each.lower()).ratio() for each in final_list]
                index= np.argmax(output)
                # print(output[index])
                if np.round(output[index], 2) > threshold:
                    return final_list[index], np.round(output[index], 2)
                else:
                    return input
            else:
                raise InvalidWord()
        except InvalidWord:
            print("Please give proper word as input")



# word_handler= WordCorrection()
# word_handler.load(input_words=['Commercially', 'available', 'development', 'Discontinued', 'Production', 'Ready', 'Samples', 'Prototype'])
#
# # print(word_handler.custom_list)
# # word_handler.remove(words=['agile','sample'])
# # print(word_handler.custom_list)
#
# result= word_handler.correct(input='develop', threshold=0.75)
# print(result)
