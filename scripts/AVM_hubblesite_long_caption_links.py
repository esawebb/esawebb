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

import hubblesite as hb

def get_root(link):
    '''
    example: from http://hubblesite.org/newsarchive/..... get http://hubblesite.org
    '''
    off = len('http://')
    end = off + link[off:].find('/')
    return link[:end]
    
    
def get_ranking(link):
    ''' get's a long_caption_link like ..../2011/23/ and returns 2011*1000 + 23 as a sort of ranking to determine which link was first'''
    s = link.split('/')
    return int(s[-2])*1000 + int(s[-1])

def remove_quotes(text):
    if text[0] == '"': text = text[1:]
    if text[-1] == '"': text = text[:-1]
    return text

def similar_titles(titles):
    result = False
    titles[0] = remove_quotes(titles[0])
    titles[1] = remove_quotes(titles[1])    
    titles[0] = hb.remove_void(titles[0].lower())
    titles[1] = hb.remove_void(titles[1].lower())    
    if titles[0] == titles[1]: result = True 
    return result
    
def analyse_links(pr_id):
    '''
    in spacetelescope.org press releases are sometimes links to the corresponding NASA Press Release
    return the link that points to hubblesite.org and contains NASA in its description
    '''
    links = None
    long_caption_link = None 
    pat = re.compile(r'<a href="(http://[^"]+)">([^<]+)</a>')
    try:
        related = Release.objects.filter(id__startswith = pr_id)[0]
        links = pat.findall(related.links)
        for link in links: 
            if link[1].find(r'''NASA''') > -1: 
                if link[0].find(r'''hubblesite''') > -1:
                    if not long_caption_link:
                        long_caption_link = link
                        # if there are more than one link to hubblesite with Nasa, take the latest
                    else:
                        if get_ranking(long_caption_link) < get_ranking(link):
                            long_caption_link = link
    except:
        pass
    return long_caption_link



def get_hubblelink(pr_id):
    link = None
    pat = re.compile(r'''.*<a href=(.*)>NASA\'s .ress .elease</a>''')
    try:
        related = Release.objects.filter(id__startswith = pr_id)[0]
        link = pat.findall(related.links)[0]
        #link = pat.search(related.links).group(1)

        if link.find(r'''http://hubblesite.org/new''') == -1: link = None
        # remove " if necessary
        if link[0]  == '''"''': link = link[1:]
        if link[-1] == '''"''': link = link[:-1] 
    except:
        pass
    return link


def get_heritagelink(pr_id):
    link = None
    pat = re.compile(r'''.*<a href=(.*)>Hubble Heritage Photo Release</a>''') 
    try:
        related = Release.objects.filter(id__startswith = pr_id)[0]
        link = pat.findall(related.links)[0]
        if link.find(r'''http://heritage.stsci.edu''') == -1: link = None
        # remove " if necessary
        if link[0]  == '''"''': link = link[1:]
        if link[-1] == '''"''': link = link[:-1] 
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


def get_long_caption_link(url, iterator, check_reachability_flag = True):
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
                if check_reachability_flag == True:
                    check =  check_reachability(long_c)
                    if check != True: long_c = None 
                break
    return long_c

    
    
def analyse(images):
    '''
    counts the number of links per long_caption_link destination
    example:
    hubblesite: 800
    heritage: 55
    '''
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

def get_related_PR(id):
    temp = ''   
    pattern = re.compile(r'''([a-z]*)([0-9]*)''')
    temp = pattern.findall(id)
    related = temp[0][0] + temp[0][1]
    iterator = temp[1][0]
    return related, iterator


if __name__ == '__main__':

    print similar_titles(['"A B\n c"', 'a b c'])
    
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)

    images = Image.objects.all()#filter(image__long_caption_link != '')
    n_images = str(len(images))
    print n_images, ' image objects'

    # analyse(images)
    
    
    # get related press releases
    # assuming that the related press releases have the same ID as the image but without the ending characters
    # heic0515a --> heic0515
    
    # then parse the related release and find the link to hubblesite
    
    # then on hubblesite, look for
              
    # then long_caption_link: <a href="/newscenter/archive/releases/2007/09/image/a/" class="intro-image-container no-zoomifyer-extra-padding"> 
    # also the link to the thumb: <img class="icon" style="margin: 0px;" src="http://imgsrc.hubblesite.org/hu/db/images/hs-2007-09-a-small_web.jpg" alt="The Colorful Demise of a Sun-like Star"><span>Go to image download page</span>
    

            
    hcount = 0
    savecount = 0
    # get long_caption_links
    long_c = None
    images = Image.objects.all()# filter(id__startswith='hei')
    for image in images:
        link = None
        link_images = None
        nasa_images = None
        result = None
        long_c = None
        link_type = 'not found'
        # get only images without a long_caption_link
        if image.long_caption_link.find('http') == -1:
            
            # print '--------------------'
            # print image.id, # image.title
            # get id of related press release
            related, iterator = get_related_PR(image.id)
            # print image.id, ': get id of related press release', related
                        
            # find the link to hubblesite.org NASA Press Release
            result =  analyse_links(related)
            if result: 
                # print 'find the link to hubblesite.org NASA Press Release' , result
                link = result[0]
            
                # get link to image releases of NASA Press release
                if (link): 
                    link_images = hb.release_images(link)
                
                    # get links to individual image releases
                    if (link_images):
                        nasa_images = hb.list_links(link_images)
                        
                        # maybe there is just one link?
                        if len(nasa_images) == 1:
                            long_c = nasa_images[0][1]
                            link_type = '''single image in NASA's release images'''
                            # print 'LONG_C!', nasa_images[0]
                        
                        else:
                        # if there are more links, compare the titles    
                            for ni in nasa_images:
                                if similar_titles([image.title,ni[0]]): 
                                    long_c = ni[1]
                                    link_type = '''titles match with a NASA's release image'''
                                    # print 'TITLES match!',
                                #print ni
                            # if there was no match, use link to Press release release images as long_caption
                            if not long_c:
                                long_c = link_images
                                link_type = '''no match, using link to NASA's release images'''
                    # if no link to release images exist, use original link to NASA Press Release
                    if not link_images:
                        long_c = link
                        link_type = '''using link to NASA's Press Release, no link to NASA's release images'''
            print image.id,';\t', long_c,';\t', link_type
     
            
            if (long_c): 
                hcount = hcount + 1
                image.long_caption_link = long_c
                #print long_c, ' is reachable, saving.....'
                try:
                    image.save()
                    savecount = savecount + 1
                except:
                    print image.id, ': failed to store long_caption_link ', long_c
                    
    print str(hcount), 'long_caption_links found'
    print 'saved ', str(savecount), ' long_caption_links'
 
               