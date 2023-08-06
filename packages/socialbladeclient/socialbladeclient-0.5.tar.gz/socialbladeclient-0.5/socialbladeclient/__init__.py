from lxml import html
import re
import requests
from datetime import datetime

URL = "https://socialblade.com/youtube/channel/"
SUBSCRIBERS_PATH = '//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]/text()'
VIDEOS_VEIWS_PATH = '//*[@id="YouTubeUserTopInfoBlock"]/div[4]/span[2]/text()'



def get_data(channel_id, timeout = 5):

    headers = {'user-agent': 'socialbladeclient'}
    r = requests.post(URL+channel_id, headers = headers, timeout = timeout)

    content = html.fromstring(r.content)
    text = str(content.xpath(SUBSCRIBERS_PATH))
    if len(text) < 2:
        raise ValueError("Please make sure your channel id is valid")
    subscribers =  str(content.xpath(SUBSCRIBERS_PATH)[0]).replace(',','')
    videos_views = str(content.xpath(VIDEOS_VEIWS_PATH)[0]).replace(',','')

    

    return {'subscribers': subscribers, 'subscribers_number': subscribers_to_number(subscribers),'total_views': videos_views, 'last_updated':datetime.now()}

def subscribers_to_number(subscribers):
    number = 1
    x=subscribers[-1]
    if x.isalpha():
        if x == "K":
            number = 1000
        elif x == "M":
            number = 1000000
        return int(number * float(subscribers[0:-1]))
    return int(subscribers)

 
