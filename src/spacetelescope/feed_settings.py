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

class VideoFeedSettings ():
    title = 'Spacetelescope.org Video Feed'
    link = '/videos/'
    description = 'The Latest Videos from Spacetelescope.org'
    enclosure_resources = {    ''   : 'resource_hd720p_screen',
                                'hd' : 'resource_hd720p_screen',
                                'sd' : 'resource_vodcast',
                                'fullhd': 'resource_hd1080p_screen'}

class ReleaseFeedSettings ():
    title = 'Hubble News'
    link = '/news/'
    description = "The latest news about astronomy and the NASA/ESA Hubble Space Telescope"
    
    
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