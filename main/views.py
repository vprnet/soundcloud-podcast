import os
import time
from main import app
from flask import render_template, request
from config import FREEZER_BASE_URL
from config import SOUNDCLOUD_API,SOUNDCLOUD_META,SEARCH_FOR
from datetime import datetime
from datetime import timedelta
from xml.sax.saxutils import escape
import soundcloud

os.environ['TZ'] = 'America/New_York'

def fix_time(time):
    cleanTimestamp = datetime.strptime(time, '%Y/%m/%d %H:%M:%S +0000')
    offsetHours = -5
    localTimestamp = cleanTimestamp + timedelta(hours = offsetHours)
    finalTimestamp =  datetime.strftime(localTimestamp,'%a, %d %b %Y %H:%M:%S +0000')
    return finalTimestamp

def escape_obj(obj):
    for key, value in obj.iteritems():
        if type(obj[key]) is str:
            obj[key] = escape(value)
        if type(obj[key]) is dict:
            for k, v in obj[key].iteritems():
                if type(obj[key][k]) is str:
                    obj[key][k] = escape(v)

@app.route('/')
def index():
    client = soundcloud.Client(
        client_id = SOUNDCLOUD_API['client_id'],
        client_secret = SOUNDCLOUD_API['client_secret'],
        username = SOUNDCLOUD_API['username'],
        password = SOUNDCLOUD_API['password']
    )
    my_tracks = []
    limit = 50
    url = '/me/tracks'
    order = 'created_at'
    tracks = client.get(
        url,
        q = SEARCH_FOR,
        order = order,
        limit = limit
    )
    # for some reason sometimes the SC API returns the tracks that are not mine,
    # so we're also going to get my info and verify that track.user_id = my id
    me = client.get('/me')
    for track in tracks:
        if SEARCH_FOR.lower() in track.title.lower() and track.downloadable and track.user_id == me.id:
            my_tracks.append({
                'title': escape(track.title),
                'permalink_url': escape(track.permalink_url),
                'download_url': escape(track.download_url.replace('https','http') + '?client_id=' + SOUNDCLOUD_API['client_id']), #https urls do not validate in feed validators?
                'enclosure_url' : 'http://feeds.soundcloud.com/stream/' + str(track.id) + '-' + track.permalink + '.mp3',
                'description': escape(track.description),
                'original_content_size': track.original_content_size,
                'created_at': fix_time(track.created_at),
                'duration': int(round(track.duration * .001))
            })

    pub_date = my_tracks[0]['created_at'] if len(my_tracks) > 0 else datetime
    escape_obj(SOUNDCLOUD_META)

    return render_template('podcast.rss',
        pub_date = pub_date,
        meta = SOUNDCLOUD_META,
        my_tracks = my_tracks)
