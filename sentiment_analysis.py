from nltk.tokenize import sent_tokenize,word_tokenize,PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer , WordNetLemmatizer
import nltk
import numpy
##import matplotlib

#tokenizing
s="This is a great iPhone. But its very expensive. Samsung is much better."
cust_toke=PunktSentenceTokenizer()
tok_sentences=cust_toke.tokenize(s)


s1=word_tokenize(s)

print s1[0]
#print (sent_tokenize(s))
stop_words=set(stopwords.words("english"))


#pos tagging takes in a list of words
#Lemmatizer works better than stemming
stop_removed=[]
ps=PorterStemmer()
lem=WordNetLemmatizer()
temp=[]
for words in s1 :
    if words not in stop_words :
        temp.append(lem.lemmatize(words))
temp=nltk.pos_tag(temp)
print temp

##
##chunkGram= r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
####chunkGram= r"""Chunk: {<WRB.?>}"""
##chunkParser=nltk.RegexpParser(chunkGram)
##chunked=chunkParser.parse(temp)
##chunked.draw()

##namedEnt= nltk.ne_chunk(temp)
##namedEnt.draw()
