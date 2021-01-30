import re
import mmap
import timeit



COMMON_PREPOSITIONS = ["ab", "ob", "e", "ex", "sed", "aut"]


#VERBS
firstConjPresentReg = ["o$","s$","t$","mus$","tis$","nt$"]
firstConjImperfectReg =  ["bam$","bas$","bat$","bamus$","batis$","bant$"]
firstConjFutureReg =  ["bo$","abis$","abit$","abimus$","abitis$","bunt$"]
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
        self.conjunction = False

    def __str__(self):
        if self.pntmv == [0,0,0,0,0]:
            print("Parsing. ")
            self.parse()
            
        
        returnPhrase = "Word:" + self.word +  " Type:" + str(self.type) + " Definition:" + str(self.definition) + " Conjunction:" + str(self.conjunction)
        returnPhrase += str(" "+ self.parsePNTMV())

        return returnPhrase
    
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
                if  self.ifVerb() is False:
                    print("error")
                    return False
        
    #Determines the word type (verb, noun, etc using regex)

    def ifPrep(self):
        if self.word in COMMON_PREPOSITIONS:
            return True
        else:
            return False
    
    def ifConj(self):
        queRegex = re.compile('[^\s]+que\b')
        if re.search(queRegex, self.word):
            self.conjunction = True
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
                    if y >= 3:
                        self.pntmv = [y+1%3, 2, x + 1, 1, 1]
                        flag = True
                    else:
                        self.pntmv = [y+1%3, 1, x + 1, 1, 1]
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
            print(x)
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



def mmap_io_find(word):
    filename = "DICTLINE.GEN"
    with open(filename, "r+b") as f:
            map_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    bytesword = bytes(" " + word + " ", 'utf-8')
    for line in iter(map_file.readline, b""):
        if bytesword in line:
            # print(line.decode('utf-8'))
            yield line.decode("utf-8")

def tester(N):
    for x in range(N):
        starttime = timeit.default_timer()
        print("The start time is :",starttime)
        x = latinWord("amaverant")
        print(x)
        fin = timeit.default_timer() - starttime
        print("The time difference is :", fin)
        yield fin

x = tester(200)
print(min(x))