#multinomial naive bayes: a worked example youtube


import numpy as np
import os

directory = "/train/spam"
words = set()
for filename in os.listdir(directory):
  text_zone = False
  with open(filename) as file:
    for line in file:
      if "X-Spam-Level:" in line:
        text_zone = True
      if text_zone:
        