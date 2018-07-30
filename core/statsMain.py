import json
import os
import datetime
import time
import statsYoutube as stats
from statsYoutube import youtube_integration as integration




if __name__ == "__main__":
    
    baseDir = os.path.dirname(os.path.abspath(__file__)) + '/'

    '''Load API keys'''
    with open(baseDir + '../api-keys.json') as f:
        keys = json.load(f)

    '''Load config-timeline.json'''
    with open(baseDir + '../config-users.json') as fileName:
        confs = json.load(fileName)
    
    '''Set vars'''
    outputFolder = baseDir+confs['temp_output']
    publishers = confs['publishers']
    currDate = time.strftime("%d-%m-%Y")
    start = datetime.datetime.now()

    '''Send request for each publisher'''
    for publisher in publishers:
        
        pubStart = datetime.datetime.now()
        
        currPub = publisher['_youtube_user']
        pubName = publisher['name']
        isChannel = publisher['isChannel']

        outputFile=outputFolder+currPub.lower()+currDate+'-yt.json'

        if publisher['isChannel'] is False:
            integration(currPub, pubName, outputFile, keys)
        else:
            print('Channel API is not implemented! Wait for updates... :D ')
            print('\n')

        pubEnd = datetime.datetime.now()

        print("Process Finished for: "+ pubName + " in " +str(pubEnd-pubStart))
        print('\n')

    end = datetime.datetime.now()
    print("Total elapsed time: "+str(end-start))


