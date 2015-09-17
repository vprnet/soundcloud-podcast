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
	localTimestamp = cleanTimestamp + timedelta(hours=offsetHours)
	finalTimestamp =  datetime.strftime(localTimestamp,'%a, %d %b %Y %H:%M:%S +0000')  
	return finalTimestamp

def escape_obj(obj):
	for key, value in obj.iteritems():
		if type(obj[key]) is str:
			obj[key] = escape(value)
		if type(obj[key]) is dict:
			for k,v in obj[key].iteritems():
				if type(obj[key][k]) is str:
					obj[key][k] = escape(v)

@app.route('/')
def index():
    client = soundcloud.Client(client_id=SOUNDCLOUD_API['client_id'],
    client_secret=SOUNDCLOUD_API['client_secret'],
    username=SOUNDCLOUD_API['username'],
    password=SOUNDCLOUD_API['password'])
    my_tracks = []
    meta = escape_obj(SOUNDCLOUD_META)
    num_tracks = 50
    sc_offset=0
    returned_tracks=num_tracks
    while (returned_tracks>0):
	    tracks = client.get('/me/tracks', q=SEARCH_FOR, order='created_at', limit=num_tracks,offset=sc_offset)
	    sc_offset = sc_offset + num_tracks
	    returned_tracks = len(tracks)
	    for track in tracks:
	    	if track.title.lower()==SEARCH_FOR and track.downloadable :
				d = {'title': escape(track.title),
				'permalink_url': escape(track.permalink_url),
				'download_url': escape(track.download_url.replace('https','http') + '?client_id='+SOUNDCLOUD_API['client_id']), #https urls do not validate in feed validators?
				'description': escape(track.description),
				'original_content_size': track.original_content_size,
				'created_at': fix_time(track.created_at),
				'duration': int(round(track.duration*.001))}
				my_tracks.append(d)

    if len(my_tracks) > 0:
    	for idx, track in enumerate(my_tracks):
    		if 0==idx :
    			pub_date = track['created_at']

    return render_template('podcast.rss',
    	pub_date=pub_date,
    	meta=SOUNDCLOUD_META,
    	my_tracks=my_tracks)
