import os
import sys
import re
import datetime
import pandas as pd


def monthSpanish2English(month):
    """
    monthSpanish2English gets a string describing the full month name in 
    Spanish and returns an integer representing this month.

    Args:
        month (string): inout string like febrero etc

    Returns:
        int: integer corresponding to month in Spanish (2 for Febrero etc)
    """
    output=None
    monthsSpa=['enero','febrero','marzo','abril','mayo','junio','julio',
    'agosto','septiembre','octubre','noviembre','diciembre']
    monthsEngNum=range(1,13,1)
    monthsDict=dict(zip(monthsSpa,monthsEngNum))
    try:
        output=monthsDict[month.lower()]
    except KeyError:
        print("no existe el mes "+str(month))
    return output
    
def quoteClassifier(quote):
    output=True
    upat = r'\w+'
    patsearcher=re.compile(upat)
    dummy=patsearcher.findall(quote)
    if len(dummy)>1:
        pass
    else:
        output=False
    return output

def wordCleaner(inputtext):
    
    output=inputtext
    upat = r'\w+'
    patsearcher = re.compile(upat)
    dummy = patsearcher.findall(inputtext)
    if len(dummy)==1:
        output=dummy[0]
    return output

def dateParser(inputtext):
    """
    dateParser parses a string from a kindle clipping file into a datetime

    Args:
        inputtext (string): string that comes from kindle clip file
        like: 3 de febrero de 2017 18:57:07

    Returns:
        [datetime datetime]: datetime from string (original in Spanish)
    """
    output=None
    try:
        dummy=str(inputtext).split()
        #print(dummy[-1])
        month=int(monthSpanish2English(dummy[2]))
        dtime=dummy[-1].split(":")
        dtimeh=int(dtime[0])
        dtimem = int(dtime[1])
        dtimes = int(dtime[2])
        output = datetime.datetime(int(dummy[4]),month ,int(dummy[0]),
                dtimeh,dtimem,dtimes)

    except:
        pass
    return output

    

def citationParser(quote):
    """
    citationParser parses a kindle clip stored on a list
    into a dictionary

    Args:
        quote (string list): [list containing the different parts of a quote]

    Returns:
        dict: [dict with author, title, quote, date as keys]
    """
    l=len(quote)
    qparsed={}
    booktitleline=str(quote[0])[:-1]
    quoteposline=str(quote[1])[:-1]
    quotetextline=str(quote[3])[:-1]
        
    patternauthor=r'[(]\D*[\)]'
    patternmarker=r'- El marcador'
    patterncomma = r'[,]'
    
    commapat = re.compile(patterncomma)
    authorpat=re.compile(patternauthor)
    markerpat=re.compile(patternmarker)
    dummymarker=markerpat.search(quoteposline)
    dummyauthor=authorpat.search(booktitleline)
    dummycomma = commapat.search(quoteposline)

    if dummymarker is None:
        
        if dummyauthor is None:
            author="unknown"
            title=booktitleline
        else:
            author=dummyauthor.group()[1:-1]
            title=booktitleline[:dummyauthor.span()[0]-1]
        createddate = quoteposline[dummycomma.span()[1]+1:]
        
        qparsed['author']=author
        qparsed['title']=title
        qparsed['quote']=quotetextline
        qparsed['date'] = dateParser(createddate)

    else:
        pass
    return qparsed

class quoteParser:
    """
     A class tha reads a Amazon Kindle's My Clippings.txt file
     and parses all the underlined things into a pandas dataframe
     with the following columns: author, title, quote and date
     It assumes the file is written in Spanish, so the dates in the file
     are parsed to datetime type. The quotes are classified as True Quotes 
     using the naive criteria: if it has more than one word, is a quote, 
     otherwise is not. It it isnt a quote, the column cleanword stores the 
     word clean, without any punctuation etc. An example is shown in another 
     file with a main function. 
    """
    def __init__(self,filename):
        self.filename=filename
    def getDataFrame(self):
        output=pd.DataFrame()
        print("attempt to read file " + self.filename)
        try:
            c = 0
            dummylist = []
            dummydict = {}
            with open(self.filename, "r") as f:
                while True:
                    dummy = f.readline()
                    if not dummy:
                        break
                    elif (dummy == "==========\n"):
                        c += 1
                        dummydict[c] = citationParser(dummylist)
                        dummylist = []

                    else:
                        dummylist.append(dummy)
                        
                print(str(c) + " notes")
            dffordb = pd.DataFrame.from_dict(
                dummydict, orient='index')
            dffordb['isquote'] = dffordb.apply(
                lambda x: quoteClassifier(x['quote']), axis=1)
            dffordb['cleanword'] = dffordb.apply(
                lambda x: '' if x['isquote'] else wordCleaner(x['quote']), axis=1)
            output=dffordb
        except:
            
            sys.exit("wrong file name")
        return output
