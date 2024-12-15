import nltk
import csv
import random
from nltk.tokenize import word_tokenize

##docs=(word_tokenize(Test),'neg')

with open('commentcsv.csv') as csvfile :
    csvReader=csv.reader(csvfile)
    for row in csvReader :
        comment=row[3:]
        fcomm=""
        for com in comment :
            fcomm=fcomm+com
        print (word_tokenize(fcomm),row[3])
        break

