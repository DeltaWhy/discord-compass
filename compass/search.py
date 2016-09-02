from compass.bot import command
from googleapiclient.discovery import build
import os
import urllib.parse
import urllib.request
import json

cse = build('customsearch', 'v1', developerKey=os.environ['GOOGLE_KEY']).cse()
yt = build('youtube', 'v3', developerKey=os.environ['GOOGLE_KEY']).search()

@command('google', 'g', 'search')
def google(*args):
    """
    Search Google.
    """
    res = cse.list(q=' '.join(args), cx=os.environ['GOOGLE_CSE_CX']).execute()
    if 'items' not in res or not res['items']:
        return "No results."
    return res['items'][0]['title'] + '\n' + res['items'][0]['link']

@command('image', 'i')
def image(*args):
    """
    Search Google Images.
    """
    res = cse.list(q=' '.join(args), searchType='image', cx=os.environ['GOOGLE_CSE_CX']).execute()
    if 'items' not in res or not res['items']:
        return "No results."
    return res['items'][0]['link']

@command('lmgtfy', 'gtfy')
def lmgtfy(*args):
    """
    Lets you Google that for someone.
    """
    return 'http://lmgtfy.com/?q=' + urllib.parse.quote_plus(' '.join(args))

@command('ddg', 'duckduckgo', 'duck')
def ddg(*args):
    """
    Use DuckDuckGo !bangs or instant answers.
    Not a web search.
    """
    res = urllib.request.urlopen('https://api.duckduckgo.com/?' +
            urllib.parse.urlencode({'q': ' '.join(args),
                'format': 'json',
                'no_redirect': 1}))
    j = json.loads(res.read().decode('utf-8'))
    res.close()

    if 'Redirect' in j and j['Redirect']:
        return j['Redirect']
    elif 'Results' in j and j['Results']:
        r = j['Results'][0]
        return r['Text'] + '\n' + r['FirstURL']
    else:
        return "No results."

@command('youtube', 'yt')
def youtube(*args):
    """
    Search YouTube videos.
    """
    res = yt.list(part='snippet', q=' '.join(args), type='video').execute()
    if 'items' not in res or not res['items']:
        return "No results."
    return res['items'][0]['snippet']['title'] + '\nhttps://www.youtube.com/watch?v=' + res['items'][0]['id']['videoId']
