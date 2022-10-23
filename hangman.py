# assignment: programming assignment 1
# author: Cheuk Yan Cherry Li
# date: Oct 7, 2022
# file: hangman.py is a program that allow user to play hangman game which the user need to guess the correct secret word
# input: user will input the size of the word and the number of lives they would like to have, the letter they guess, and if they want to replay the game
# output: the progam will print the game introduction, and the instruction to guide the user to play the hangman game
from random import choice, random
import random

dictionary_file = "dictionary.txt"   # make a dictionary.txt in the same folder where hangman.py is located

# function to print the letters that user have chosen
def display_chosen_letter(chosen_list):
  return ("Letters chosen: " + chosen_list)

# get user prenfrence on replaying the game or not
def cont_game():
  user_prefrence = input("Would you like to play again [Y/N]?" ).upper()
  print()
  while 1:
    try:
      if user_prefrence == "N":
        print()
        print("Goodbye!")
        survive = False
        return survive
        break
      elif user_prefrence == "Y":
        survive = True
        return survive
        break
      else:
        raise TypeError
    except TypeError:
      print ("Not a valid input")
      break

# a function to ask user to guess a letter
def guess():
  while True:
    try:
      user_input = input("Please choose a new letter > ")
      print()
      if user_input.isalpha() and len(user_input) == 1:
        return (user_input.upper())
      else:
        raise TypeError
    except TypeError:
        user_input = guess()
        return (user_input.upper())
        break

# dictionary keys are word sizes (1, 2, 3, 4, …, 12), and values are lists of words
# for example, dictionary = { 2 : ['Ms', 'ad'], 3 : ['cat', 'dog', 'sun'] }
# if a word has the size more than 12 letters, put it into the list with the key equal to 12

def import_dictionary (filename) :
  dictionary = {}
  max_size = 12
  for i in range (2, max_size+1):
    dictionary[i] = []
  try :
    file = open(filename, "r")
    for word in file:
      word = word.lstrip()
      if (len(word) > 12):
        dictionary[12].append(word[0:len(word)-1])
      elif (len(word)-1) in dictionary:
        dictionary[len(word)-1].append(word[0:len(word)-1])
    file.close()
  except Exception :
    print("Unable to read: " + filename)
  return dictionary

# print the dictionary (use only for debugging)
def print_dictionary (dictionary) :
  max_size = 12
  print(dictionary)

# get options size and lives from the user, use try-except statements for wrong input
def get_game_options () :
  try:
    size = input("Please choose a size of a word to be guessed [3 - 12, default any size]: \n")
    if size.isnumeric() == False or int(size) < 3 or int(size) > 12:
      size = random.randint(3,12)
      print("A dictionary word of any size will be chosen.")
    else:
      print("The word size is set to " + str(size) + ".")

    lives = input("Please choose a number of lives [1 - 10, default 5]: \n")
    if lives.isnumeric() == False or int(lives) < 1 or int(lives) > 10:
      lives = "5"
    print("You have " + lives + " lives.")
  except ValueError:
    print("Not a valid integer")
  return (int(size), int(lives))

# MAIN

if __name__ == '__main__' :
    # make a dictionary from a dictionary file
    dictionary = import_dictionary(dictionary_file)

    # print the dictionary (use only for debugging)
    # print_dictionary(dictionary)    # remove after debugging the dictionary function import_dictionary

    # print a game introduction
    print ("Welcome to the Hangman Game!")

    # START MAIN LOOP (OUTER PROGRAM LOOP)
    survive = True
    while (survive == True):

      # set up game options (the word size and number of lives)
      game_option = get_game_options ()
      lives = game_option[1]
      str_lives = str(lives)
      size = game_option[0]

      # select a word from a dictionary (according to the game options)
      # use choice() function that selects an item from a list randomly, for example:
      # mylist = ['apple', 'banana', 'orange', 'strawberry']
      # word = choice(mylist)
      secret_word = choice(dictionary[size]).upper()
      secret_list = list(secret_word)
      
      # format and print the game interface:
      # Letters chosen: E, S, P                list of chosen letters
      # __ P P __ E    lives: 4   XOOOO        hidden word and lives
      #print (display_chosen_letter(chosen_list))
      #print(' '.join(underscore_list) + remain_lives)
      chosen = {}
      chosen_letter = []
      chosen_list = ', '.join(filter(lambda x: x if x is not None else '', chosen_letter))
      remain_lives = "   lives: " + str_lives + "      " + "O" * lives 
      underscore_list = []
      for i in secret_list:
        underscore_list.append("__")
      for i in range(len(secret_list)):
        if "-" == secret_list[i]:
          underscore_list[i] = "-"
      print (display_chosen_letter(chosen_list))
      print(' '.join(underscore_list) + remain_lives)

      # START GAME LOOP   (INNER PROGRAM LOOP)
      while remain_lives.count("O") > 0 and underscore_list != secret_list:
      
        # ask the user to guess a letter
        user_input = guess()
      
        # update the list of chosen letters
        if user_input not in chosen.keys():
          chosen[user_input] = 0
          chosen_letter.append(user_input)
          chosen_list = ', '.join(filter(lambda x: x if x is not None else '', chosen_letter))
        else:
          chosen[user_input] += 1
          
        # if the letter is correct update the hidden word,
        # else update the number of lives
        # and print interactive messages 
        if chosen[user_input] > 0:
          print()
          print("You have already chosen this letter.")
        elif chosen[user_input] == 0:
          if user_input in secret_list:
            print()
            print("You guessed right!")
            for i in range(len(secret_list)):
              if user_input == secret_list[i]:
                underscore_list[i] = user_input
            print (display_chosen_letter(chosen_list))
            print(' '.join(underscore_list) + remain_lives)
          elif user_input not in secret_list:
            print()
            print("You guessed wrong, you lost one life.")
            lives -= 1
            remain_lives = remain_lives.replace(str_lives, str(lives))
            str_lives = str(lives)
            remain_lives = remain_lives.replace("O", "X", 1)
            print (display_chosen_letter(chosen_list))
            print(' '.join(underscore_list) + remain_lives)
        
       
      # check if the user guesses the word correctly or lost all lives,
      # if yes finish the game
      if underscore_list == secret_list:
        print("Congratulations!!! You won! The word is " + secret_word + "!")
        survive = False
      if remain_lives.count("O") == 0: 
        print("You lost! The word is " + secret_word + "!")
        survive = False

      # ask if the user wants to continue playing, 
      # if yes start a new game, otherwise terminate the program
      survive = cont_game()