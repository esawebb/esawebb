#
# eso.org
# Copyright 2011 ESO
#
# -*- coding: utf-8 -*-
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

import datetime

def new_id(long_caption_link):
    '''
    creates 2003-28-a out of the long caption link ...eases/2003/28/image/a/
    returns '-' if failed
    '''
    id = ''
    pattern = re.compile('.*?([0-9]*?)/([0-9]*?)/image/([a-z]?)')
    try:
        results = pattern.findall(long_caption_link)[0]
        id  = results[0]+'-'+results[1]
        if results[2] != '': id = id +'-'+results[2]
    except:
        id = '-'
    return id


def process_objects(objs):
    for obj in objs:
        print obj.id
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
    
        
        