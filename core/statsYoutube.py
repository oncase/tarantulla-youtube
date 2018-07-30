import urllib.request as request
import json
import os
import datetime
import time


def output(data, mode = 'JSON', file_name = './youtube_videos.json'):
    '''
        Youtube Output Write Function
    '''
    with open (file_name, 'a', encoding='utf-8') as file:
        file.write(str(data))
        file.write("\n")



def do_request(url):
    '''
        Youtube Send Request
    '''
    if url is not None:
        content = request.urlopen(url).read()
        return json.loads(content.decode('utf-8'))



def get_channel_id(userName, key, BASE_URL='https://www.googleapis.com/youtube/v3/channels?part=contentDetails&maxResults=50'):
    '''
        Youtube Get Channel ID
    '''    
    
    API_URL=BASE_URL+'&forUsername='+userName+'&key='+key
    data = do_request(API_URL)
    
    return data



def get_channel_analytics(userName, key, BASE_URL='https://content.googleapis.com/youtube/v3/channels?part=statistics'):
    '''
        Youtube Get Channel Analytics
    '''
    API_URL=BASE_URL+'&key='+key+'&forUsername='+userName
    data = do_request(API_URL)
    return data



def get_video_links(playlistId, key, BASE_URL='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50'):
    '''
        Youtube Get Video Links
    '''
    n = 0
    yt_dict_out=[]
    API_URL=BASE_URL+'&playlistId='+playlistId+'&key='+key
    data = do_request(API_URL)

    if 'nextPageToken' in data:
        try:
            next_page=data['nextPageToken']
            qtd_results = data['pageInfo']['totalResults']            
            while (n < qtd_results) and ('nextPageToken' in data):
                for i in range(0, len(data['items'])):
                    resultDict={}
                    resultDict['publishedAt'] = data['items'][i]['snippet']['publishedAt']
                    resultDict['channelId'] = data['items'][i]['snippet']['channelId']
                    resultDict['title'] = data['items'][i]['snippet']['title']
                    resultDict['description'] = data['items'][i]['snippet']['description']
                    resultDict['channelTitle'] = data['items'][i]['snippet']['channelTitle']
                    resultDict['playlistId'] = data['items'][i]['snippet']['playlistId']
                    resultDict['videoId'] = data['items'][i]['snippet']['resourceId']['videoId']
                    yt_dict_out.append(resultDict)
                    n+=1
                    
                API_URL=BASE_URL+'&playlistId='+playlistId+'&key='+key+'&pageToken='+next_page
                data = do_request(API_URL)
                next_page=data['nextPageToken']
        except KeyError as e:                
            for i in range(0, len(data['items'])):
                resultDict={}
                resultDict['publishedAt'] = data['items'][i]['snippet']['publishedAt']
                resultDict['channelId'] = data['items'][i]['snippet']['channelId']
                resultDict['title'] = data['items'][i]['snippet']['title']
                resultDict['description'] = data['items'][i]['snippet']['description']
                resultDict['channelTitle'] = data['items'][i]['snippet']['channelTitle']
                resultDict['playlistId'] = data['items'][i]['snippet']['playlistId']
                resultDict['videoId'] = data['items'][i]['snippet']['resourceId']['videoId']
                yt_dict_out.append(resultDict)
                n+=1            
            print("Downloading video links... Total number of loaded links: " + str(n))           
    return yt_dict_out
    


def get_video_analytics(videoId, key, BASE_URL='https://content.googleapis.com/youtube/v3/videos?part=statistics&maxResults=50'):
    '''
        Youtube Get Video Analytics
    '''
    API_URL = BASE_URL+'&key='+key+'&id='+videoId
    data = do_request(API_URL)
    return data



def youtube_integration(ytUser, name, outputFolder, keys):
    '''
        Youtube Orchestration Process - Publisher Full Load
    '''

    print ("Tarantulla Youtube - Starting... - Publisher: " + name)
    print("Process Started at: "+ time.strftime("%d/%m/%Y %H:%M:%S"))

    yt_channel_data = get_channel_id(userName = ytUser, key=keys["YTAPIKEY"])
    yt_channel_stats = get_channel_analytics (userName = ytUser, key=keys["YTAPIKEY"])
    uploads_id = yt_channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = get_video_links(playlistId=uploads_id, key=keys["YTAPIKEY"])

    for video in videos:

        print("Collecting " + name + " : " + str(videos.index(video)) + " statistics collected", end='\r')        
        videoAnalytics = get_video_analytics(video['videoId'], key=keys["YTAPIKEY"])
        
        try:            
            video['views']=videoAnalytics['items'][0]['statistics']['viewCount']            
        except KeyError as e:
            print('Field viewCount - Not Found in JSON')
            video['views']=str(0)
        
        try:
            video['likes']=videoAnalytics['items'][0]['statistics']['likeCount']
        except KeyError as e:
            print('Field likeCount - Not Found in JSON')
            video['likes']=str(0)
            
        try:
            video['dislikes']=videoAnalytics['items'][0]['statistics']['dislikeCount']
        except KeyError as e:
            print('Field dislikeCount - Not Found in JSON')
            video['dislikes']=str(0)

        try:
            video['favorite']=videoAnalytics['items'][0]['statistics']['favoriteCount']
        except KeyError as e:
            print('Field favoriteCount - Not Found in JSON')
            video['favorite']=str(0)

        try:
            video['comment']=videoAnalytics['items'][0]['statistics']['commentCount']
        except KeyError as e:
            print('Field commentCount - Not Found in JSON')
            print('WARN - Comments can be disabled for this video - If you Want to verify follow this link https://www.youtube.com/watch?v=' + video['videoId'])
            video['comment']=str(0)

        video['channelSubscribers']=yt_channel_stats['items'][0]['statistics']['subscriberCount']
        video['name'] = name

    for content in videos:
        output(content, file_name = outputFolder)


    print("Process Finished at: "+ time.strftime("%d/%m/%Y %H:%M:%S"))
