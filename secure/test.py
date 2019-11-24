import logging
import threading
import time
from spellchecker import SpellChecker

spell = SpellChecker()
spell2 = SpellChecker(language=None,case_sensitive=False)


def checkPosition(characterS):
    """checkpostionCharacter"""
    line1 = ("q w e r t y u i o p [ ] \ ").split()
    line2 = ("a s d f g h j k l ; ' ").split()
    line3 = ("z x c v b n m , . / ").split()
    
    ##################################### define value #####################################

    if characterS in line1:
        for j in range(len(line1)):
            if(characterS == line1[j]):
                if(j in [0, 10, 11, 12]):
                    if(j == 0):
                        return ['q', 'w', 'a', 's']
                    elif(j == 10):
                        return ['p', '[', ']', ';', "'"]
                    elif(j == 11):
                        return ['[', ']', line1[-1], "'"]
                    elif(j == 12):
                        return [']', line1[-1]]
                else:
                    return [line1[j-1], line1[j], line1[j+1], line2[j-1], line2[j], line2[j+1]]

    # if character in line 1 on keyboard


    elif(characterS in line2):
        for j in range(len(line2)):
            if(characterS == line2[j]):
                if(j in [0, 10]):
                    if(j == 0):
                        return ['q', 'w', 'a', 's', 'z', 'x']
                    elif(j == 10):
                        return ['[', ']', ';', "'", '.', '/']
                else:
                    return [line1[j-1], line1[j], line1[j+1], line2[j-1], line2[j], line2[j+1], line3[j-1], line3[j], line3[j+1]]
    
    # if character in line 2 on keyboard

    elif(characterS in line3):
        for j in range(len(line3)):
            if(characterS == line3[j]):
                if(j in [0, 9]):
                    if(j == 0):
                        return ['a', 's', 'z', 'x']
                    elif(j == 9):
                        return [';', "'", '.', '/']
                else:
                    return [line2[j-1], line2[j], line2[j+1], line3[j-1], line3[j], line3[j+1]]

    # if character in line 3 on keyboard


def generate(list1,list2):
    """generate prob word"""
    output = []
    specChar = [';', '"', "'", '/', '\\', '[', ']', ',','.',':']

    ##################################### define value #####################################

    for i in list1:
        if(i not in specChar):
            for j in list2:
                if(j not in specChar):
                    output.append(i+j)

    return output


def getAllprobWord(arrayText,genList,text):
    """ return all prob word """
    genList = arrayText[0]

    ##################################### define value #####################################

    for i in range(len(arrayText)-1):
        genList = generate(genList,arrayText[i+1])
    return genList


def getMapAllProbinCheckSpell(correctWord,text):
    """get var from map in rockyou"""
    return list(spell2.known(correctWord)),list(spell.known([spell2.correction(text)]))



def mainLoop(text):
    """mainfunction"""

    text = text.lower()

    genList = []
    # all probability word
    arrayText = []
    # get position of character

    ##################################### define value #####################################

    for i in text:arrayText.append(checkPosition(i))
    # create postion all array
    # ex: [[q w a s], [q w e a s d]]

    genList = getAllprobWord(arrayText,genList,text)
    # all prob

    misspell = spell.unknown(genList)
    # sep not word


    correctWord = list(filter(lambda x: x not in misspell, genList))
    correctionWordnotMap = correctWord
    # delete missepl in all brob

    spell2.word_frequency.load_text_file('test.txt')
    # add top 500 rockyou
    
    correctWord,caseInput = getMapAllProbinCheckSpell(correctWord,text)
    if(caseInput not in correctWord and len(caseInput) != 0 ):correctWord.append(caseInput[0])

    # check in correctword+top500badpassword
    # print(correctionWordnotMap)
    # print(correctWord)

    # get arrayText for get list of position
    # get getList for get All prob word ** more than 1m if len text >= 6
    # get correction for get word map from rockyou
    # caseInput for case like abizail
    # print(arrayText)
    # print('loving' in genList)
    print(correctWord) 
    
mainLoop(input())
