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
# Mantis 12079 helper to find information on hubblesite.org 
#*************************************************************************************************************

import re
import urllib2 

import socket
timeout = 60
socket.setdefaulttimeout(timeout)

def get_redirect(link):
    #returns link from urllib2.urlopen() or if this is not possilbe None is returned
    redirect = ''
    try:
        remote   = urllib2.urlopen(link) 
        redirect = remote.geturl()
    except:
        redirect = None            
    return redirect

def remove_void(text):
    '''
    removes double whites and linebreaks
    '''
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = ' '.join(text.split())
    return text

def release_images(link):
    '''
    returns link to the release images section for a press release link
    '''
    link = get_redirect(link)
    
    if link.find('image') == -1:
        if link[-1] == '/':
            link = link + 'image/'
        else:
            link = link + '/image/'
    else:
        end = link.find('image')
        link = link[:end] + 'image/'
    return link

def list_links(url_images):   # [^>]
    '''
    list all links and titles for image releases
    example: http://hubblesite.org/newscenter/archive/releases/2005/37/image/:
    ['A Giant Hubble Mosaic of the Crab Nebula', '/newscenter/archive/releases/2005/37/image/a/']
    ['Crab Nebula: a Dead Star Creates Celestial Havoc', '/newscenter/archive/releases/2005/37/image/b/']
    '''
    site = urllib2.urlopen(url_images)
    text = site.read()
    
    # remove all linebreaks and double whitespace
    text = remove_void(text)
     
    pat = re.compile(r'(<a href="(/newscenter/archive/[^"]+)">)[\s]?<span class="link">(.*?)</span>.*?</a>')  
    links = None
    try:
        links = pat.findall(text)
    except:
        pass
    newlinks = []
    for l in links:
        description = l[2]
        link        = l[1]
        newl = [description,link]
        newlinks.append(newl)
    return newlinks
      

if __name__ == '__main__':
    #routines to test the helper functions
    print "list_links:"
    release = r'''http://hubblesite.org/newscenter/archive/releases/2005/37'''
   # release = r'''http://hubblesite.org/newscenter/archive/releases/2008/16/image/ce/'''
    images = release_images(release)
    

    links = list_links(images)

    print images
    c = 0
    if links: 
        for link in links: 
            c = c + 1
            print c, '   ', link
      