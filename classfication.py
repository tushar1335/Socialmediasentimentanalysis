import nltk
import random
import csv
from nltk.corpus import movie_reviews
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


docs=[]

##for category in movie_reviews.categories() :
##    for fileid in movie_reviews.fileids(category) :
##        docs.append((list(movie_reviews.words(fileid)),category))
##random.shuffle(docs)

with open('commentcsv.csv') as csvfile :
    csvReader=csv.reader(csvfile)
    for row in csvReader :
        comment=row[3:]
        fcomm=""
        for com in comment :
            fcomm=fcomm+com
        docs.append((word_tokenize(fcomm),row[3]))


##all_words=[]
##allowed_word_types = ["J"]
##for word in movie_reviews.words():
##    all_words.append(word.lower())

all_words=[]
allowed_word_types = ["J"]
for c in docs:
    for word in c[0] :
        if word not in all_words :
            all_words.append(word.lower())

new_words=[]
pos=nltk.pos_tag(all_words)
for w in pos :
    if w[1][0] in allowed_word_types :
            new_words.append(w[0].lower())
new_words=nltk.FreqDist(new_words)


##word_features=list(new_words.keys())[:5000]
word_features=list(new_words.keys())
save_word_features = open("word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()


#HERE


##word_featuresf=open("word_features5k.pickle", "rb")
##word_features = pickle.load(word_featuresf)
##word_featuresf.close()

##save_documents = open("documents.pickle","wb")
##pickle.dump(docs, save_documents)
##save_documents.close()
##
##documents_f = open("documents.pickle", "rb")
##docs = pickle.load(documents_f)
##documents_f.close()


def find_features(document) :
    words=set(document)
    features={}
    for w in word_features:
        features[w]=(w in words)
    return features

featuresets=[(find_features(rev),category) for (rev,category) in docs ]


random.shuffle(featuresets)
##training_set=featuresets[:1900]
##testing_set=featuresets[1900:]
training_set=featuresets[:300]
testing_set=featuresets[301:]

    
classifier=nltk.NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features(15)
##classf=open("naivebayes.pickle","rb")
##classifier=pickle.load(classf)
##classf.close()
##save_classifier=open("naivebayes.pickle","wb")
##pickle.dump(classifier,save_classifier)
##save_classifier.close()
print (nltk.classify.accuracy(classifier,testing_set))*100



MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

##save_classifier = open("MNB_classifier5k.pickle","wb")
##pickle.dump(MNB_classifier, save_classifier)
##save_classifier.close()
##
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

##save_classifier = open("BernoulliNB_classifier5k.pickle","wb")
##pickle.dump(BernoulliNB_classifier, save_classifier)
##save_classifier.close()
##
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

##save_classifier = open("LogisticRegression_classifier5k.pickle","wb")
##pickle.dump(LogisticRegression_classifier, save_classifier)
##save_classifier.close()
##
##
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

##save_classifier = open("LinearSVC_classifier5k.pickle","wb")
##pickle.dump(LinearSVC_classifier, save_classifier)
##save_classifier.close()
##
SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

##save_classifier = open("SGDC_classifier5k.pickle","wb")
##pickle.dump(SGDC_classifier, save_classifier)
##save_classifier.close()


#here
##open_file = open("MNB_classifier5k.pickle", "rb")
##MNB_classifier = pickle.load(open_file)
##open_file.close()
##
##
##
##open_file = open("BernoulliNB_classifier5k.pickle", "rb")
##BernoulliNB_classifier = pickle.load(open_file)
##open_file.close()
##
##
##open_file = open("LogisticRegression_classifier5k.pickle", "rb")
##LogisticRegression_classifier = pickle.load(open_file)
##open_file.close()
##
##
##open_file = open("LinearSVC_classifier5k.pickle", "rb")
##LinearSVC_classifier = pickle.load(open_file)
##open_file.close()
##
##
##open_file = open("SGDC_classifier5k.pickle", "rb")
##SGDC_classifier = pickle.load(open_file)
##open_file.close()




voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

def sentiment(text):
    print text
    feats={c:True for c in word_tokenize(text)}
##    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)

##print sentiment("This movie was awesome. The acting was great , plot was wonderful,and there were python")
##print sentiment("Amazing movie , wonderful beautiful interesting great")
##print sentiment("Shitty movie. Boring. Awful and direction was bad. will not watch again")
##print sentiment ("This is one movie that no one needs to relive.")
##print sentiment ("Doesn't seem to enjoy its own ridiculous concept enough, and yet refuses to stage any set pieces that feel honestly scary either.")
##print sentiment ("The movie is too long, too violent, too silly-too everything. Yet for those who enjoyed the original Kingsman, it is a more than adequate second act. To put it another way: First time satire, second time farce.")
##print sentiment ("Forced jokes, ridiculous characters and a bad plot may get a laugh and maybe thats enough for many.")
##print sentiment("Kingsman: The Golden Circle continues to supply the dapper, yet high-octane action and sequences and a surplus of starpower. The film may suffer from predictability but the innovative cinematography is an entertaining touch even if it doesn't exceed the levels of the first.")
##print sentiment("It's such a great performance that you wish Muschietti had eased up on the CGI and just let Skarsgård do the talking.")
##print sentiment("Will certainly please fans of the original and terrify a new generation.")
##print sentiment("I'm writing this not so much as a critic but as an ordinary moviegoer, experiencing Proustian transport via an old-fashioned scary movie executed by a team of filmmakers and actors at the top of their game.")
##print sentiment ("If you copy something, try to better than the original. That's the only way to justify your good intention of giving the best concept or idea that already exist.﻿")
trial="beautiful best upgrade miss awesome want"
##w=nltk.word_tokenize(trial)
print sentiment(trial)
##print classifier.classify(find_features(w))
##
