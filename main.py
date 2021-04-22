import os
import sys

from parsekindlenotes import quoteParser
params = sys.argv

if __name__ == "__main__":
    
    try:
        if len(params) > 1:
            filename = str(params[1])
            qparser=quoteParser(filename)
            dfout=qparser.getDataFrame()
            print("***************")
            print("***************")
            print(dfout)
            dfout.to_csv("test.csv")
        else:
            print("no input file path selected")
    except:
        sys.exit("missing input file")
        
