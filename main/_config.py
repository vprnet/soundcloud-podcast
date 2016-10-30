import os
import inspect

# Flask
DEBUG = True

# Amazon S3 Settings
AWS_KEY = ''
AWS_SECRET_KEY = ''
AWS_BUCKET = 'www.vpr.net'
AWS_DIRECTORY = 'sandbox/app/'

SOUNDCLOUD_API = {
    "client_id": "",
    "client_secret": "",
    "username": "",
    "password": ""
}
SEARCH_FOR = '' # the track title to search for (SC filter by tag does not work wel)
SOUNDCLOUD_META = {
    "title" : "", # the title of this podcast
    "description" : "", # podcast description
    "link" : "", # link to website for this resource (i.e. fairbanksmuseum.org/...)
    "atom_link": "", # the url for this podcast (e.g. http://www.vpr.net/sandbox/this-podcast/)
    "webmaster" : "podmaster@vpr.net (VPR PodMaster)",
    "itunes_author" : "Vermont Public Radio",
    "itunes_subtitle" : "",
    "itunes_summary" : "",
    "itunes_owner" : {
        "name":"Eye On The Sky",
        "email" : "podmaster@vpr.net"
    },
    "itunes_image" : "", # 1400x1400 image/icon for this podcast - hosted by apps/ or sandbox/dirname/static/images/
    "itunes_category_1": "", # a valid itunes category
    "itunes_category_2": "", # a valid itunes subcategory
    "itunes_keywords": ""
}

# Cache Settings (units in seconds)
STATIC_EXPIRES = 60 * 24 * 3600
HTML_EXPIRES = 3600

# Frozen Flask
FREEZER_DEFAULT_MIMETYPE = 'application/rss+xml'
FREEZER_IGNORE_MIMETYPE_WARNINGS = True
FREEZER_DESTINATION = 'build'
FREEZER_BASE_URL = 'http://%s/%s' % (AWS_BUCKET, AWS_DIRECTORY)
FREEZER_STATIC_IGNORE = [
    'Gruntfile*',
    'node_modules',
    'package.json',
    'dev',
    '.sass-cache'
]

WEBFACTION_PATH = AWS_DIRECTORY

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/'
