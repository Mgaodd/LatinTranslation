import re
import mmap
import timeit
from lemminflect import getInflection





COMMON_PREPOSITIONS = ["ab", "ob", "e", "ex", "sed", "aut"]


#VERBS
firstConjPresentReg = ["o$","as$","at$","amus$","atis$","ant$"]
firstConjImperfectReg =  ["abam$","abas$","abat$","abamus$","abatis$","abant$"]
firstConjFutureReg =  ["abo$","abis$","abit$","abimus$","abitis$","bunt$"]
firstConjPerfectReg =  ["i$","isti$","it$","imus$","istis$","erunt$"]
firstConjPluperfectReg = ["eram$","eras$","erat$","eramus$","eratis$","erant$"]
firstConjFuturePerfectReg = ["ero$","eris$","erit$","erimus$","eritis$","erint$"]
firstConjReg = [firstConjPresentReg, firstConjImperfectReg, firstConjFutureReg, firstConjPerfectReg, firstConjPluperfectReg, firstConjFuturePerfectReg]





class latinWord:
    
    def __init__(self, word):
        self.word = word
        self.type = ""
        self.definition = ""
        self.pntmv = [0,0,0,0,0]
        self.cng = 0
        self.stem = ""
        self.conjDec = 0
        self.conjunction = False


    def __str__(self):
        if self.pntmv == [0,0,0,0,0]:
            print("Parsing. ")
            self.parse()
        if self.definition == "":
            self.defineWord()   
        
        returnPhrase = "Word:" + self.word +  " Type:" + str(self.type) + " Definition:" + str(self.definition) + " Conjunction:" + str(self.conjunction) + " Stem:" + str(self.stem)
        returnPhrase += str(" "+ self.parsePNTMV())
        return returnPhrase

    def defineWord(self):
        line = self.findWord(self.stem)
        defStart = re.search(" [^ ] [^ ] [^ ] [^ ] [^ ] ", line).span()[1]
        definitions = line[defStart:]
        print(definitions)
        self.definition = definitions[0:re.search(",|;", definitions).span()[1] - 1]
        print(self.definition)

    

    def translateWord(self):
        if self.pntmv == [0,0,0,0,0]:
            print("Parsing. ")
            self.parse()
        if self.definition == "":
            self.defineWord()
        
        if self.type == "V":
            self.translateVerb()

    def translateVerb(self):
        # person,number,tense,mood,voice = self.pntmv
        print(self.pntmv)
        person = self.pntmv[0]
        number = self.pntmv[1]
        tense = self.pntmv[2]
        mood = self.pntmv[3]
        voice = self.pntmv[4]


        string = ""

        if person == 1 and number == 1:
            string += "I"
        if person == 2 and number == 1:
            string += "You"
        if person == 3 and number == 1:
            string += "It"
        if person == 1 and number == 2:
            string += "We"
        if person == 2 and number == 2:
            string += "You all"
        if person == 3 and number == 2:
            string += "They"

        if tense == 1:
            string += " "+self.definition
        
        if tense == 2 and number == 2 or person == 2 and tense == 2:
            string += " were "
            inflected = getInflection(self.definition, tag = 'VBG')[0]
            string += inflected
        if tense == 2 and number == 1 and person != 2:
            string += " was "
            inflected = getInflection(self.definition, tag = 'VBG')[0]
            string += inflected

        if tense == 3:
            string += " will " + self.definition
        if tense == 4:
            string += " have "
            inflected = getInflection(self.definition, tag = 'VBN')[0]
            string += inflected
        if tense == 5:
            string += " had "
            inflected = getInflection(self.definition, tag = 'VBD')[0]
            string += inflected
        if tense == 6:
            string += " will have "
            inflected = getInflection(self.definition, tag = 'VBN')[0]
            string +=  inflected
        
        print(string + ".")
        return string
            



    def findWord(self, word):
        filename = "DICTLINE.GEN"
        if word[0:1] == "i":
            word = re.sub('i', 'j', word, 1)
        

        with open(filename, "r+b") as f:
                map_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        bytesword = bytes(" " + word + " ", 'utf-8')

        for line in iter(map_file.readline, b""):
            flag = False
            if bytesword in line:
                line = line.decode("utf-8")
                string = re.sub(" {1,}", ",", line)
                splitString = string.split(",")
                for x in range(6):
                    if splitString[x] == word:
                        if self.type in splitString:
                            findV = re.search(",V,", string).span()[1]
                            definedVal = string[findV: findV + 1]
                            if str(self.conjDec) in definedVal:
                                flag = True
                if flag:
                    return line
    
    def parsePNTMV(self):
        pntmv =  self.pntmv
        string = ""
        person =  pntmv[0]
        if person == 1 or person == 4:
            string+= str(" 1st")
        elif person == 2 or person == 5:
            string+= str(" 2nd")
        elif person == 3 or person == 6:
            string+= str(" 3rd")

        number = pntmv[1]
        if number == 1:
            string+= str(" Singular")
        elif number == 2:
            string+= str(" Plural")
        
        tense = pntmv[2]
        if tense == 1:
            string+= str(" Present")
        elif tense == 2:
            string+= str(" Imperfect")
        elif tense == 3:
            string+= str(" Future")
        elif tense == 4:
            string+= str(" Perfect")
        elif tense == 5:
            string+= str(" Pluperfect")
        elif tense == 6:
            string+= str(" Future_Perfect")

        return string
        
        
    def parse(self):
        if self.ifPrep() is False:
            if  self.ifConj() is False:
                if self.ifNoun() is False:
                    if self.ifVerb() is False:
                        print("error")
                        return False
        
    #Determines the word type (verb, noun, etc using regex)
    firstDecReg = []
    def ifNoun(self):
        flag = False
        for x in 
    def ifPrep(self):
        if self.word in COMMON_PREPOSITIONS:
            return True
        else:
            return False
    
    def ifConj(self):
        queRegex = re.compile('[^\s]+que\b')
        if re.search(queRegex, self.word):
            self.conjunction = True
            self.word = self.word[0:re.search(queRegex, self.word)[0]]
        else:
            return False
    
    def ifVerb(self):
        flag = False
        for x in firstConjReg:
            for y in x:
                if re.search(y, self.word):
                    flag = True
                    if self.firstConj() is True:
                        break
                    else:
                        print("Error.")
                        break
            if flag:
                break         
    
    def firstConj(self):
        max = 0
        flag = False
        for x in range(0,6):
            for y in range(0,6):
                if re.search(firstConjReg[x][y], self.word):
                    curr = len(firstConjReg[x][y])
                    if curr > max:
                        max = curr
                    else:
                        continue
                    self.stem = self.word[0:re.search(firstConjReg[x][y], self.word).span()[0]]

                    if y >= 3:
                        self.pntmv = [(y%3)+1, 2, x + 1, 1, 1]
                        self.type = "V"
                        self.conjDec = 1
                        flag = True
                    else:
                        self.pntmv = [(y%3)+1, 1, x + 1, 1, 1]
                        self.type = "V"
                        self.conjDec = 1
                        flag = True
        return flag


        
class latinPhrase:
    def __init__(self, phrase):
        self.wordCount = 0
        self.string =  phrase
        self.words = []
        self.createWords()

    def createWords(self):
    
        spliiterEx = re.compile(" ")
        phrases = self.string

        phrases = re.split(spliiterEx, phrases)
        for x in phrases:
            if x == None:
                continue

            self.words+= str(latinWord(x))
            self.wordCount += 1

    def __str__(self):
        return "Phrase:" + self.string + " Word Count:" + str(self.wordCount)


class latinScentence:
    def __init__(self, scentence):
        self.phrasesCount = 0
        self.string = scentence
        self.phrases = []
        self.createPhrases(self.string)
    
    def cleanInput(self, input):
        cleanerEx = re.compile("[^a-zA-Z ,.;]")
        input = re.sub(cleanerEx,"", input)
        return input

    def createPhrases(self, input):
        splitterEx = re.compile("[,;.]")
        input = re.split(splitterEx, input)
        for x in input:
            x = x.strip()
            if re.search("[ *] | [,*]", x) or x == None:
                continue
            self.phrases+= str(latinPhrase(x))  
            self.phrasesCount += 1
    
    def printPhrases(self):
        for x in self.phrases:
            print(x)
            print("")

    def __str__(self):
        return "Scentence: " + self.string + " Phrases: " + str(self.phrasesCount)
 



# userIn = input("Here: ")
# lat = latinScentence(userIn)
# print(lat)





def tester(N):
    for x in range(N):
        starttime = timeit.default_timer()
        print("The start time is :",starttime)
        x = latinWord("amaverant")
        print(x)
        fin = timeit.default_timer() - starttime
        print("The time difference is :", fin)
        yield fin

latinWord(input(": ")).translateWord()

