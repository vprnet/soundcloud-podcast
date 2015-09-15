import os
import time
from main import app
from flask import render_template, request
from config import FREEZER_BASE_URL
from config import SOUNDCLOUD_API,SOUNDCLOUD_META,SEARCH_FOR
from datetime import datetime
from datetime import timedelta
import soundcloud

os.environ['TZ'] = 'America/New_York'

def fixTime(time):
	cleanTimestamp = datetime.strptime(time, '%Y/%m/%d %H:%M:%S +0000')
	offsetHours = -5
	localTimestamp = cleanTimestamp + timedelta(hours=offsetHours)
	finalTimestamp =  datetime.strftime(localTimestamp,'%a, %d %b %Y %H:%M:%S +0000')  
	return finalTimestamp

@app.route('/')
def index():
    page_title = 'VPR App Template'
    page_url = FREEZER_BASE_URL.rstrip('/') + request.path
    client = soundcloud.Client(client_id=SOUNDCLOUD_API['client_id'],
    client_secret=SOUNDCLOUD_API['client_secret'],
    username=SOUNDCLOUD_API['username'],
    password=SOUNDCLOUD_API['password'])
    my_tracks = []
    num_tracks = 50
    sc_offset=0
    returned_tracks=num_tracks
    while (returned_tracks>0):
	    tracks = client.get('/me/tracks', q=SEARCH_FOR, order='created_at', limit=num_tracks,offset=sc_offset)
	    sc_offset = sc_offset + num_tracks
	    returned_tracks = len(tracks)
	    for track in tracks:
	    	if track.title.lower()==SEARCH_FOR and track.downloadable :
				d = {'title': track.title,
				'permalink_url': track.permalink_url,
				'download_url': track.download_url + '?client_id='+SOUNDCLOUD_API['client_id'],
				'description': track.description,
				'original_content_size': track.original_content_size,
				'created_at': fixTime(track.created_at),
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
