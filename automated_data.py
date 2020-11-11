#import libraries 
import bs4 as bs 
import urllib.request
import pandas as pd
import requests 
from bs4 import BeautifulSoup
import boto3

# list of unknow election results 
states=['AZ', 'FL', 'GA', 'IA', 'ME', 'MI', 'NC', 'NV', 'OH', 'PA', 'TX', 'WI']
#create a lists   to save urls 
urls=[]
# loop through state list and append the state to the url 
for state in states:
  url = "https://eu.usatoday.com/elections/results/race/2020-11-03-presidential-"
  url += state +'-0/'
  urls.append(url)

# create empty list to append candidate information 
table_list=[]

# loop through urls 
for url in urls:
  # return source code 
  sauce = urllib.request.urlopen(url).read()
  #return bs object
  soup = bs.BeautifulSoup(sauce,"lxml")
  # scrape table 
  table = soup.table
  # find all the rows 
  table_rows = table.find_all('tr')
  
  # loop through rows 
  for tr in table_rows:
    # find all the td 
    td = tr.find_all('td')
    # get text for each row and column
    row = [i.text for i in td]
    # append to list 
    table_list.append(row)

def candidate_df(name):
  """
  Takes list_name as in `table_list` candidate name 
  and name of candate and returns a data frame with 
  the relevant info 
  """
  list_name =[]
  # loop through ou list and retrivr only biden info 
  for item in table_list:
    if name in item:
      list_name.append(item)
  #create data frame 
  df= pd.DataFrame(list_name, columns = ['Candidate', 'Total votes', 'Percentage of votes'])
  # add state info 
  df['State'] = states
  return df

# create biden df 
df_biden = candidate_df('Joe\nBiden (D)')

# create trum dataframe 
df_trump = candidate_df('Donald\nTrump (R) *')

# if csv file is already in S3 bucket read the file from the desited url
df = pd.read_csv('https://usa-election-bucket.s3.amazonaws.com/politics_new.csv')


df_unsure = df.loc[df['state'].isin(states)]
# drop party column to create a new one depending on results 
df_unsure = df_unsure.drop('party', axis = 1)

#create a secon data frame with the rest of the information
df_sure = df.loc[~df['state'].isin(states)]

# make a list for comparision 
biden_votes = list(df_biden['Percentage of votes'])
trump_votes = list(df_trump['Percentage of votes'])

# loop trhoug lists 
party=[]
#loop trhough votes lists to create a list with party name  in case of candidate andvantage 
for vote in range(len(biden_votes)):
  # if biden has more pecentage of votes append democrat
  if biden_votes[vote] > trump_votes[vote]:
    party.append('democrat')
  # if trump has more percentage append republican 
  elif biden_votes[vote] < trump_votes[vote]: 
    party.append('republican')
  # if hey are equal append unsure 
  else:
    party.append('unsure')

# add new results to df_unsure 
df_unsure['party'] = party

df = pd.concat([df_sure, df_unsure])
#save dataframe 
df.to_csv('politics1.csv', index = False )

s3 = boto3.resource(
    service_name ='s3',
    aws_access_key_id='Your AWS key id',
    aws_secret_access_key='your AWS secret access key'
)
s3.meta.client.upload_file('politics1.csv', 'your AWS bucket name', 'politics_new.csv', ExtraArgs={'ACL':'public-read'})