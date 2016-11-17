#multinomial naive bayes: a worked example youtube


import numpy as np
import os

directory = "train/spam"
words = set()
for filename in os.listdir(directory):
  text_zone = False
  with open(os.path.join(directory,filename)) as file:
    for line in file:
      if "X-Spam-Level:" in line:
        text_zone = True
        print ("hello")
      if text_zone:
        words.add( set(line.split()) )
    print(words)
    quit()
        