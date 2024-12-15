#!/usr/bin/python

# Usage example:
# python comments.py --videoid='<video_id>' --text='<text>'
import string
import httplib2
import os
import sys
import io
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

f=io.open("TrainingData.txt","w+",encoding='utf-8')

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-discoverydocument.json", "r") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

def writethreads(results,chname,pro) :
  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    #remove punctuation from comments
    punc=set(string.punctuation)
    ftweet=""
    for char in text :
      if char not in punc :
        ftweet=ftweet+char
    lines=ftweet.lower().splitlines()
    text=' '.join([line.strip() for line in lines])
    f.write(pro+";"+chname+";"+author+";"+text+"\n")
    #print "Comment by %s: %s" % (author, text)
  
# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube, video_id,chname,pro):
  idlist=[]
  results = youtube.commentThreads().list(part="snippet",
    videoId=video_id,
    textFormat="plainText",
    maxResults=100
  ).execute()
  writethreads(results,chname,pro)
  for i in range(len(results["items"])) :
    idlist.append(results["items"][i]["id"])
  if "nextPageToken" in results.keys() :
    pt=results["nextPageToken"]
    np=True
  else :
    np=False
  while np :
    results = youtube.commentThreads().list(part="snippet",
      videoId=video_id,
      textFormat="plainText",
      pageToken=pt,
      maxResults=100).execute()
    writethreads(results,chname,pro)
    for i in range (len(results["items"])) :
      idlist.append(results["items"][i]["id"])
    if "nextPageToken" in results.keys() :
      pt=results["nextPageToken"]
    else :
      np=False
  return idlist


# Call the API's comments.list method to list the existing comment replies.
def get_comments(youtube, parent_id,chname,pro):
  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  for item in results["items"]:
    author = item["snippet"]["authorDisplayName"]
    text = item["snippet"]["textDisplay"]
    #remove punctuation from comments
    punc=set(string.punctuation)
    ftweet=""
    for char in text :
      if char not in punc :
        ftweet=ftweet+char
    lines=ftweet.lower().splitlines()
    text=' '.join([line.strip() for line in lines])
    f.write(pro+";"+chname+";"+author+";"+text+"\n")
    #print "Comment by %s: %s" % (author, text)
  return results["items"]

if __name__ == "__main__":
  cccount=0
  # The "videoid" option specifies the YouTube video ID that uniquely
  # identifies the video for which the comment will be inserted.
  argparser.add_argument("--videoid",
    help="Required; ID for video for which the comment will be inserted.")
  # The "text" option specifies the text that will be used as comment.
  #argparser.add_argument("--text", help="Required; text that will be used as comment.")
  args = argparser.parse_args()

##  if not args.videoid:
##    exit("Please specify videoid using the --videoid= parameter.")
##  if not args.text:
##    exit("Please specify text using the --text= parameter.")

  youtube = get_authenticated_service(args)
  # All the available methods are used in sequence just for the sake of an example.
  try:
    vid={'iPhoneX':("j8wTNuviku0 MrMobile"),
         'SamsungGalaxyNote8':("LVup8cO7rPQ MrMobile"),
         'LGV30':("tbdrA_2vASw MrMobile")
         }
##    vid={'EssentialPhone':("xywcBJuV7tk MrMobile"),
##         'MotoZ2Force':("emQ6RChmdR8 MrMobile"),
##         'OnePlus5':("gxkHHxYrMWw MrMobile"),
##         'HTCU11':("lad1V4W_rmI MrMobile")}
##    vid={'iPhoneX':("j8wTNuviku0 MrMobile")}
    #j8wTNuviku0
    for key , value in vid.iteritems() :
      tempv=value.split(" ")
      video_comment_threads = get_comment_threads(youtube,tempv[0],tempv[1],key)
      for i in range (0,len(video_comment_threads)) :
        parent_id = video_comment_threads[i]
        video_comments = get_comments(youtube, parent_id,tempv[1],key)
    f.close()
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  else:
    print "Inserted, listed, updated, moderated, marked and deleted comments."
