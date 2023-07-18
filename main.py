# Why have I made this, what's the point? What's my purpose? what the fuck am I doing?
import nltk
import language_tool_python
from nltk.corpus import wordnet as wn
from numpy import full
import requests
from bs4 import BeautifulSoup
import random
import re
import pyttsx3
import openai
import datetime

date = datetime.datetime.now()


engine = pyttsx3.init()
def gpt3(sentence):
    #GPT-3
    openai.api_key = "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"

    response = openai.Edit.create(
        engine="text-davinci-edit-001", 
        input=sentence, 
        instruction="Make the sentence like Alex Jones and grammatically correct",
        temperature=1,
        top_p = 1,
    )

    content = response.choices[0].text.split(".")
    return response.choices[0].text
def randLine(fname):
	lines=open(fname).read().splitlines()
	return random.choice(lines)

open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/fromNews.txt', 'w').close()
open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Nouns.txt', 'w').close()
open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Adjectives.txt', 'w').close()
open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Verbs.txt', 'w').close()
open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Others.txt', 'w').close()
open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/ProperNouns.txt', 'w').close()
open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/AlexJones.txt', 'w').close()
titles = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/fromNews.txt', 'a')
url = 'https://www.bbc.com/news'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all('h3')
unwanted = ['BBC World News TV', 'BBC World Service Radio',
			'News daily newsletter', 'Mobile app', 'Get in touch']

for x in list(dict.fromkeys(headlines)):
	if x.text.strip() not in unwanted:
		titles.write(x.text.strip() + "\n")

titles.close()

nouns = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Nouns.txt', 'a')
verbs = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Verbs.txt', 'a')
adjectives = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Adjectives.txt', 'a')
others = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Others.txt', 'a')
properNouns = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/ProperNouns.txt', 'a')
POS = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/POS.txt', 'a')
AJ = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/AlexJones.txt', 'a')


readLines = open('/Users/shashankraghuraj/BigProjects/AlexJonesRobot/fromNews.txt', 'r')
Lines = readLines.readlines()
 
# Strips the newline character
string_check= re.compile("'[@_!#$%^&*()<>?/\|}{~:]") #regex for special characters
for line in Lines:
    tokens = nltk.word_tokenize(line)
    tagged = nltk.pos_tag(tokens)
    newList = []
    classification = ""
    for t in tagged:
        if t[1] == "NNS":
            classification = "noun"
            nouns.write(t[0] + "\n")
        elif t[1] == "NNP":
            classification = "Proper Noun"
            properNouns.write(t[0] + "\n")
        elif t[1] == "VB":
            classification = "verb"
            verbs.write(t[0] + "\n")
        elif t[1] == "JJ":
            classification = "adjective"
            adjectives.write(t[0] + "\n")
        elif t[1] == "MD":
            classification = "other"
            others.write(t[0] + "\n")
        elif t[1] == "POS":
            classification = "POS"
            POS.write(t[0] + "\n")
        # print("{}: {}".format(t[0], classification))

nouns.close()
verbs.close()
adjectives.close()
others.close()

def makeSentence():
    sentence = ""
    #Subject + Adjective + Verb + Object
    noun = randLine("/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Nouns.txt")
    verb = randLine("/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Verbs.txt")
    adjective = randLine("/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Adjectives.txt")
    other = randLine("/Users/shashankraghuraj/BigProjects/AlexJonesRobot/CC.txt")
    properNouns = randLine("/Users/shashankraghuraj/BigProjects/AlexJonesRobot/Nouns.txt")
    POS = randLine("/Users/shashankraghuraj/BigProjects/AlexJonesRobot/POS.txt")
    sentence = properNouns + POS + " "  + verb  + " " + adjective + " " + noun + "."
    return sentence

print("Processing...")
fullSentence = "" #keeps track of the full sentence
count = 0 #keeps track of the number of sentences
while count < 100:
    print("Iterations:\t" + str(count))
    if count > 85:
        response = gpt3(makeSentence())
        #print(response)
        fullSentence = fullSentence + response + " "
    count+=1


fullSentence = "BREAKING NEWS"+ str(date.day) + "/" + str(date.month) + "/" + str(date.year) +": \n" + fullSentence
print(fullSentence)
AJ.write(fullSentence)