# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Feed settings for website project

class VideoPodcastFeedSettings ():
    title = 'Spacetelescope.org Video Feed'
    link = '/videos/'
    description = 'The Latest Videos from Spacetelescope.org'
    enclosure_resources = {    ''   : 'resource_hd720p_screen',
                                'hd' : 'resource_hd720p_screen',
                                'sd' : 'resource_vodcast',
                                'fullhd': 'resource_hd1080p_screen'}
    override_guids = { 'heic0705a': u'http://www.spacetelescope.org/videos/heic1007a/',
                    'heic0706a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast35a.m4v',
                    'heic0707a': u'http://www.spacetelescope.org/videos/vodcast/heic1006a.m4v',
                    'heic0708a': u'http://www.spacetelescope.org/videos/vodcast/heic1003a.m4v',
                    'heic0709a': u'http://www.spacetelescope.org/videos/vodcast/heic0917a.m4v',
                    'hubblecast06a': u'http://www.spacetelescope.org/videos/vodcast/heic0912a.m4v',
                    'heic0712a': u'http://www.spacetelescope.org/videos/vodcast/heic0910a.m4v',
                    'heic0714a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast29a.m4v',
                    'heic0715a': u'http://www.spacetelescope.org/videos/vodcast/heic0907a.m4v',
                    'hubblecast10a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast27a.m4v',
                    'heic0719a': u'http://www.spacetelescope.org/videos/vodcast/heic0901c.m4v',
                    'heic0720a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast25a.m4v',
                    'heic0804a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast24a.m4v',
                    'heic0807a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast23a.m4v',
                    'heic0809a': u'http://www.spacetelescope.org/videos/vodcast/heic0821a.m4v',
                    'heic0810a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast21a.m4v',
                    'hubblecast17a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast20a.m4v',
                    'heic0817a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast19a.m4v',
                    'hubblecast19a': u'http://www.spacetelescope.org/videos/vodcast/heic0817a.m4v',
                    'hubblecast20a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast17a.m4v',
                    'hubblecast21a': u'http://www.spacetelescope.org/videos/vodcast/heic0810a.m4v',
                    'heic0821a': u'http://www.spacetelescope.org/videos/vodcast/heic0809a.m4v',
                    'hubblecast23a': u'http://www.spacetelescope.org/videos/vodcast/heic0807a.m4v',
                    'hubblecast24a': u'http://www.spacetelescope.org/videos/vodcast/heic0804a.m4v',
                    'hubblecast25a': u'http://www.spacetelescope.org/videos/vodcast/heic0720a.m4v',
                    'heic0901c': u'http://www.spacetelescope.org/videos/vodcast/heic0719a.m4v',
                    'hubblecast27a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast10a.m4v',
                    'heic0907a': u'http://www.spacetelescope.org/videos/vodcast/heic0715a.m4v',
                    'hubblecast29a': u'http://www.spacetelescope.org/videos/vodcast/heic0714a.m4v',
                    'heic0910a': u'http://www.spacetelescope.org/videos/vodcast/heic0712a.m4v',
                    'heic0912a': u'http://www.spacetelescope.org/videos/vodcast/hubblecast06a.m4v',
                    'heic0917a': u'http://www.spacetelescope.org/videos/vodcast/heic0709a.m4v',
                    'heic1003a': u'http://www.spacetelescope.org/videos/vodcast/heic0708a.m4v',
                    'heic1006a': u'http://www.spacetelescope.org/videos/vodcast/heic0707a.m4v',
                    'hubblecast35a': u'http://www.spacetelescope.org/videos/vodcast/heic0706a.m4v',
                    'heic1007a': u'http://www.spacetelescope.org/videos/vodcast/heic0705a.m4v'
                    }
    
    
    
    
class ReleaseFeedSettings ():
    title = 'Hubble News'
    link = '/news/'
    description = "The latest news about astronomy and the NASA/ESA Hubble Space Telescope"
    
    override_guids = {
        'heic1007': u'http://www.spacetelescope.org/news/heic1007/',
        'heic1006': u'http://www.spacetelescope.org/news/html/heic1006.html',
        'heic1005': u'http://www.spacetelescope.org/news/html/heic1005.html',
        'heic1004': u'http://www.spacetelescope.org/news/html/heic1004.html',
        'heic1003': u'http://www.spacetelescope.org/news/html/heic1003.html',
        'heic1002': u'http://www.spacetelescope.org/news/html/heic1002.html',
        'heic1001': u'http://www.spacetelescope.org/news/html/heic1001.html',
        'heic0918': u'http://www.spacetelescope.org/news/html/heic0918.html',
        'heic0917': u'http://www.spacetelescope.org/news/html/heic0917.html',
        'heic0916': u'http://www.spacetelescope.org/news/html/heic0916.html',
        'heic0915': u'http://www.spacetelescope.org/news/html/heic0915.html',
        'heic0914': u'http://www.spacetelescope.org/news/html/heic0914.html',
        'heic0913': u'http://www.spacetelescope.org/news/html/heic0913.html',
        'heic0912': u'http://www.spacetelescope.org/news/html/heic0912.html',
        'heic0911': u'http://www.spacetelescope.org/news/html/heic0911.html',
        'heic0910': u'http://www.spacetelescope.org/news/html/heic0910.html',
        'heic0909': u'http://www.spacetelescope.org/news/html/heic0909.html',
        'heic0908': u'http://www.spacetelescope.org/news/html/heic0908.html',
        'heic0907': u'http://www.spacetelescope.org/news/html/heic0907.html',
        'heic0906': u'http://www.spacetelescope.org/news/html/heic0906.html',
        'heic0905': u'http://www.spacetelescope.org/news/html/heic0905.html',
        'heic0904': u'http://www.spacetelescope.org/news/html/heic0904.html',
        'heic0903': u'http://www.spacetelescope.org/news/html/heic0903.html',
        'heic0902': u'http://www.spacetelescope.org/news/html/heic0902.html',
        'heic0901': u'http://www.spacetelescope.org/news/html/heic0901.html',
        'heic0823': u'http://www.spacetelescope.org/news/html/heic0823.html'
        }


class HubblecastFeedSettings ():
    title = 'Hubblecast %s'
    link = '/videos/hubblecast/'
    description =  'The latest news about astronomy, space, and the NASA/ESA Hubble Space Telescope'
    
    



CATEGORY_SPECIFIC_SETTINGS = {
    'hubblecast': 'HubblecastFeedSettings',
    
    }

FORMATS = {
    '': ('HD',''),
    'hd': ('HD',''),
    'sd': ('SD',''),
    'fullhd' : ('Full HD',''),
}