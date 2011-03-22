#
# -*- coding: utf-8 -*-#
# eso.org
# Copyright 2011 ESO
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis 12175: Fix release dates for images and videos
#
#
# Find wrong release_dates:
# 1) Check id with release_date - e.g. opo0214a with release date in 2010 must be wrong
# 2) Release dates with 2011-03-03 18:00-18:44 are wrong
#
# Don't bother about images connected to announcements, releases and potws.
#
# For images with long_caption_link or press_release_link follow the link and extract the date. 
#
#
#*************************************************************************************************************


from djangoplicity.utils import optionparser
from djangoplicity.media.models import Image
from djangoplicity.media.models import Video

import re
import urllib2

import logging, sys
import socket

from datetime import datetime
import pytz

import hubblesite

def convert_time():
    dt = datetime( 1993, 1, 7, 12, 00, tzinfo=pytz.timezone( 'US/Eastern' ) )
    newdt = dt.astimezone( pytz.timezone( 'Europe/Berlin' ) )
    print dt, newdt
    return


def change_datetime(obj):
    '''
    follows the long_caption_link or the press_release_link to get the correct date
    '''
    # get link to image or press release
    link = None
    success = False
    if obj.long_caption_link.find('http') > -1:
        link = obj.long_caption_link
    elif obj.press_release_link.find('http') > -1:
        link = obj.press_release_link
    
    # follow link and get new date
    if link:
        release_date = hubblesite.get_release_date(link)
        if release_date:
            try:
                print '-------------------------------------------------------'
                print obj.id, obj.release_date.strftime('%Y-%B-%d %I:%M %p %Z')
                release_date = release_date.astimezone( pytz.timezone( 'Europe/Berlin' ) )
                release_date = datetime.replace(release_date, tzinfo=None)
                obj.release_date = release_date
                print obj.id, obj.release_date.strftime('%Y-%B-%d %I:%M %p %Z')
                obj.save()
                success = True
            except:
                print obj.id,' save failed!'
                pass
    return success


def process_objects(objs):
    '''
    find the objects that need a correction of the release_date
    '''
    finddate1 = datetime.strptime('2011-03-03 18:00:00','%Y-%m-%d %H:%M:%S')
    finddate2 = datetime.strptime('2011-03-03 19:00:00','%Y-%m-%d %H:%M:%S')
    for obj in objs:
        # obj.release_date is a datetime object
        dt = obj.release_date
        #print dt, dt.date
        if (dt):
            if dt >= finddate1 and dt <= finddate2:
                change_datetime(obj)
    return


if __name__ == '__main__':
    logger = logging.getLogger('app.' + __name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.propagate = False
    logger.info("Fix release dates for images and videos")
    
    
    
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)


    test =  '''<h2 class="release-number"><strong>News Release Number:</strong> STScI-2006-25</h2>'''
    pattern = re.compile('''h2 class="release-number".*?:.*?>\s*(.*?)<.*?h2''')    

    process_objects(Image.objects.all())
    process_objects(Video.objects.all())
    
    convert_time()
        
        