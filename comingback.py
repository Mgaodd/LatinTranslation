import regex as re
import mmap

# Notes:
# http://latindictionary.wikidot.com/learn:sentence-1
# 

# Goal:
# Parse the scentence:
#   Puer puellam vexat.



accusativeRegEx = ['am$','as$','um$','os$','a$','em$','es$','ia$','us$','ua$']
nominativeRegEx = ['a$','ae$','r$','i$','x$','is$','e$','es$','us$','u$','ua$']
firstConjPresentReg = ["o$","as$","at$","amus$","atis$","ant$"]
firstConjImperfectReg =  ["abam$","abas$","abat$","abamus$","abatis$","abant$"]
firstConjFutureReg =  ["abo$","abis$","abit$","abimus$","abitis$","bunt$"]
firstConjPerfectReg =  ["i$","isti$","it$","imus$","istis$","erunt$"]
firstConjPluperfectReg = ["eram$","eras$","erat$","eramus$","eratis$","erant$"]
firstConjFuturePerfectReg = ["ero$","eris$","erit$","erimus$","eritis$","erint$"]
firstConjReg = [firstConjPresentReg, firstConjImperfectReg, firstConjFutureReg, firstConjPerfectReg, firstConjPluperfectReg, firstConjFuturePerfectReg]


class LatinScentence:
    def __init__(self, scentence):
        self.scentence = scentence.lower()
        self.words = []
        self.createWords()

    def __str__(self):
        return "Scentence: " + self.scentence + " Words: " + str(self.words)
    
    def createWords(self):
        words = self.scentence.split(" ")
        for x in words:
            self.words.append(LatinWord(x))

    
    def createScentence(self):
        final = ""
        #Finding Nominative
        for word in self.words:
            for tp in word.types:
                if "noun" in tp:
                    if "nominative" in tp:
                        final = final + "The " + word.define(word.word)
        
        #Finding Verb
        for word in self.words:
            print("\n", word)
            for tp in word.types:
                if "verb" in tp:
                    final = final + " did " + word.word
        
        #Finding Accusative
        for word in self.words:
            print("\n", word)
            for tp in word.types:
                if "noun" in tp:
                    if "accusative" in tp:
                        final = final + " to the " + word.word
        
        print(final + ".")

        

            




    def parseWords(self):
        for x in self.words:
            x.determineType()



    
class LatinWord:
    def __init__(self, word):
        self.word = word
        self.types = []

    def containsType(self, type, specification):
        pass;
    
    def define(self, word):
        return word
    
    def determineType(self):
        print("Determining:")
        
        for x in nominativeRegEx:
            if(re.search(x, self.word )):
                self.types.append(("noun", "nominative"))
        
        for x in accusativeRegEx:
            if(re.search(x, self.word )):
                self.types.append(("noun", "accusative"))
        
        for x in firstConjPresentReg:
            if(re.search(x, self.word )):
                self.types.append(("verb", "firstPresent"))
        

    def isVerb(self):
        pass

    def isNoun(self):
        pass
    
    def __str__(self):
        return self.word + str(self.types)
    def __repr__(self):
        return self.__str__()



x= LatinScentence("Puer puellam vexat")
x.parseWords()

print(x)

x.createScentence()


