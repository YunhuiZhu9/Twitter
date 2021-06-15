#!/usr/bin/env python
# coding: utf-8

# In[1]:


# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time


# In[2]:


bearer_token = "AAAAAAAAAAAAAAAAAAAAACQwFwEAAAAAqnfQXHa9iyCN%2BWIgk3sGVfKKepc%3DwRNGyToqBlRqwpKfTzMmSntVlfL29VMP8cf9psVNY0mqkjovNS"


# In[3]:


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# In[4]:


def create_url(keyword, start_date, end_date, max_results):
    
    search_url = "https://api.twitter.com/2/tweets/search/all" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'tweet.fields': 'id,text,author_id,created_at',
                    'next_token': {}}
    return (search_url, query_params)


# In[5]:


def connect_to_endpoint(url, headers, params, next_token):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# In[10]:


def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. Tweet ID
        tweet_id = tweet['id']

        # 4. Tweet text
        text = tweet['text']
        
        # Assemble all data in a list
        res = [author_id, created_at, tweet_id, text]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter) 


# In[8]:


data = pd.read_csv('try.csv')
Name=pd.read_csv('Name.csv')


# In[11]:


#Inputs for tweets


headers = create_headers(bearer_token)

start_time = "2006-03-21T00:00:00.000Z"  
end_time = "2021-06-14T00:00:00.000Z"

max_results = 500

#Total number of tweets we collected from the loop
total_tweets = 0



for i in range(0,2288):
    a=Name["Name"]
    name=str(a[i])
    keyword="(from:"+name+" is:retweet)"
    #keyword=str(key)
    #key="(from:"+name+"-is:retweet) OR #"+name
    #keyword=str(key)
    
    b=data["ID"]
    print (str(b[i]))

    NAME=str(b[i])+".csv"


        # Create file
    csvFile = open(NAME, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

        #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['author id', 'created at',  'id','tweet'])
    csvFile.close()

    # Inputs
    count = 0 # Counting tweets per time period
    #max_count = 100 # Max tweets per time period
    flag = True
    next_token = None
    
    # Check if flag is true
    while flag:
        # Check if max_count reached
        #if count >= max_count:
           # break
        #print("-------------------")
        #print("Token: ", next_token)
        url = create_url(keyword, start_time,end_time, max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
        #result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            next_token = json_response['meta']['next_token']
            print("Next Token: ", next_token)
            #if next_token is not None:
            append_to_csv(json_response, NAME)
            #df = pd.json_normalize(json_response['data'])
            #df.to_csv(NAME)
            print(json.dumps(json_response, indent=4, sort_keys=True))
        else:
            flag = False
            next_token = None

                
            
            #Since this is the final request, turn flag to false to move to the next time period.

        time.sleep(5)
print("Total number of results: ", total_tweets)


# In[ ]:




