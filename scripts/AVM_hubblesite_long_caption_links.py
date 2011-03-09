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
# Mantis 12079 short check which prefixes have a long_caption_link


#*************************************************************************************************************

from djangoplicity.utils import optionparser
from djangoplicity.media.models import Image
from djangoplicity.releases.models import Release

import re
import urllib2

import logging, sys
import socket
import pprint

def get_root(link):
    off = len('http://')
    end = off + link[off:].find('/')
    return link[:end]
    

def get_hubblelink(pr_id):
    link = None
    try:
        related = Release.objects.filter(id__startswith = pr_id)[0]
        link = related.links
        start = link.find('http://hubblesite.org/news')  # http://hubblesite.org/news/  or http://hubblesite.org/newscenter/archive/releases/2011/01
        end   = link[start:].find('''">''')
        if start == -1: link = '-'
        else:
            link = link[start:start+end]
    except:
        pass
    return link

def check_reachability(url):
    result = True
    
    try:
        urllib2.urlopen(url) #,data = '', timeout=5
    except urllib2.URLError, e:
        result = str(e.code) 
    return result


def get_long_caption_link(url, iterator):
    long_c = None
    try:
        remote   = urllib2.urlopen(url)
    except:
        remote  = 'timeout?'
    for line in remote:
        if line.find('<a href=') > -1:
            if line.find('''/image/''') > -1:
                look_for = '''<a href='''
                start = line.find(look_for) + len(look_for)
                end   = line[start:].find('''>''')
                long_c = line[start:end]
                if long_c[0] == '''"''': long_c = long_c[1:]
                if long_c[-1] == '''"''': long_c = long_c[:-1]
                if long_c[0] == '/': long_c = 'http://hubblesite.org' + long_c
                
                # now replace the last letter in the link with the iterator (heic0515c) /a/ --> /c/
                end = long_c.rfind('/')
                start = long_c[:end].rfind('/')
                long_c = long_c[:start] +'/' + iterator + '/'
                
                check =  check_reachability(long_c)
                if check != True: long_c = None 
                break
    return long_c

    
    
def analyse(images):
    dict = {}  #dict containing little dicts ldict
    ldict = {}
    list = []
    linkdict = {} # collects the possible roots for long_caption_links
    for image in images:
        if image.long_caption_link.find('http') == -1: continue

        list.append(image.id)

        prefix = image.id[:3]
        link   = get_root(image.long_caption_link)
        if link in linkdict:
            linkdict[link] = linkdict[link] + 1
        else: linkdict[link] = 1
        if prefix in dict:
            ldict = dict[prefix]
            if link in ldict:
                n = ldict[link]
                n = n + 1
                ldict[link] = n
            if link not in ldict:
                ldict[link] = 1
        dict[prefix] = ldict
        if not prefix in dict:
            ldict = {}
            ldict[link] = 1
            dict[prefix] = ldict
    list.sort()
    print list
    for d in dict.keys():
        print d, dict[d]
    print linkdict



if __name__ == '__main__':
    logger = logging.getLogger('app.' + __name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stderr))
    logger.propagate = False
    logger.info("get hubblesite ids")
    
    
    
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)

    images = Image.objects.all()#filter(image__long_caption_link != '')
    n_images = str(len(images))
    print n_images

    # analyse(images)
    
    
    # get related press releases
    # assuming that the related press releases have the same ID as the image but without the ending characters
    # heic0515a --> heic0515
    
    # then parse the related release and find the link to hubblesite
    
    # then on hubblesite, look for
              
    # then long_caption_link: <a href="/newscenter/archive/releases/2007/09/image/a/" class="intro-image-container no-zoomifyer-extra-padding"> 
    # also the link to the thumb: <img class="icon" style="margin: 0px;" src="http://imgsrc.hubblesite.org/hu/db/images/hs-2007-09-a-small_web.jpg" alt="The Colorful Demise of a Sun-like Star"><span>Go to image download page</span>
    
    pattern = re.compile(r'''([a-z]*)([0-9]*)''')
            
    hcount = 0
    savecount = 0
    # get long_caption_links
    long_c = None
    images = Image.objects.all()# filter(id__startswith='hei')
    for image in images:
        # get all images without a long_caption_link
        if image.long_caption_link.find('http') == -1:
            temp = pattern.findall(image.id)
            related = temp[0][0] + temp[0][1]
            iterator = temp[1][0]
            
#            # for DEBUG
#            if related != 'heic1007': continue
            
            link = get_hubblelink(related)
            if (link): long_c = get_long_caption_link(link, iterator)
            print image.id, related, link, long_c
            hcount = hcount + 1
            
            if (long_c): 
                image.long_caption_link = long_c
                print long_c, ' is reachable, saving.....'
                try:
                    image.save()
                    savecount = savecount + 1
                except:
                    print image.id, ': failed to store long_caption_link ', long_c
#                
#            # for DEBUG
#            if related == 'heic1007': break
#            
            
            
    print hcount
    print 'saved ', str(savecount), ' long_caption_links'
    
    
#        logger.info(str(count)+' / '+n_images + ' ' + image.id + ' ' + hubble_id + ' ' + middle  + ' ' + image.long_caption_link + ' ' + thumberror)
           
        
        