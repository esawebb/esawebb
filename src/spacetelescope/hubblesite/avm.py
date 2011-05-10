#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
# Authors:
#  Lars Holm Nielsen <lnielsen@eso.org>
#  Dirk Neumayer <dirk.neumayer@gmail.com>
#
#  access avm metadata as dict, source is a json file from
#  http://archdev.stsci.edu/stpr/search.php 
#
#  to get the json file:
#  for all fields goto Output Columns and push button add all, 
#  choose the maximum value in Maximum Records and
#  in Output Format choose 'File: JSON Format'
#  then press search
# 
#  TODO: ??? have a definition of avm tag names and format for versions 1.1, 1.2,... at a central place, as a dictionary or class
#***********************************************************************************************************************

import os, sys
import re
import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson as json

def load_json(json_file):
    '''
    loads the content of the given JSON file and returns it.
    '''
    json_data = None
    try:
        fp = open(json_file,'r')
        json_data = json.load(fp)
        fp.close()
    except IOError, (errno, strerror):
        logger.error("I/O error(%s): %s" % (errno, strerror))
        logger.error("Problem opening file %s, returning None" % json_file )   
    return json_data

def remove_duplicates():
    raise NotImplementedError
    return

def strings2list(strings):
    ''' converts comma (;) separated values to a list of strings
    '''
    list = None  
    if strings and strings.find(';'): list = [s.strip() for s in strings.split(';')]
    return list

def subjectcategories(strings):
    ''' skip X., return list with category objects
    '''
    print strings
    strings = strings.replace(u' &gt; ', '.')
    if strings and strings.find(','): list = [s.strip() for s in strings.split(',')]
    for l in list: 
        if l[0] == 'X': list.remove(l) 
    return list

def jsondict2avmdict(jsondict):
    ''' 
    creates an avmdict using the values of the jsondict
    TODO: add function to report if the return of json_load is different than expected (new fields, no list anymore,....)
    '''

    # Dates => DateTime object
    # Distance lly / z ? return list [ly,z CHECK order] if one is not specified use None
    # image/tiff => TIFF
    
    # in future, use this in a Deserializer function
    
    mapping = {
        # 3.1 Creator Metadata
         'Creator':                       { 'fieldname': 'Creator'},
         'CreatorURL':                    { 'fieldname': 'CreatorURL'},
         'Contact.Name':                  { 'fieldname': None,  'func': strings2list},
         'Contact.Email':                 { 'fieldname': 'Contact Email'},
         'Contact.Telephone':             { 'fieldname': 'Contact Phone'},
         'Contact.Address':               { 'fieldname': 'Contact Address'},
         'Contact.City':                  { 'fieldname': 'Contact City'},
         'Contact.StateProvince':         { 'fieldname': 'Contact State'},
         'Contact.PostalCode':            { 'fieldname': 'Contact code'},                               # TODO: ['Contact code','Contact Code'] in case they fix the typo
         'Contact.Country':               { 'fieldname': 'Contact Country'},
         'Contact.Email':                 { 'fieldname': 'Contact Email'},
         'Contact.Email':                 { 'fieldname': 'Contact Email'},
         'Rights':                        { 'fieldname': 'Usage Terms'},
        # 3.2 Content Metadata         
         'Title':                         { 'fieldname': 'Title'},
         'Headline':                      { 'fieldname': 'Headline'},
         'Description':                   { 'fieldname': 'Description'},
         'Subject.Category':              { 'fieldname': 'Subject Category', 'func': subjectcategories},                           
         'Subject.Name':                  { 'fieldname': 'Subject', 'func': strings2list},              
         'Distance':                      { 'fieldname': 'Distance', 'func': strings2list},
         'Distance.Notes':                { 'fieldname': 'Distance Notes'},
         'ReferenceURL':                  { 'fieldname': 'Press Release Images' },
         'Credit':                        { 'fieldname': 'Credit'},
         'Date':                          { 'fieldname': 'Date Created'},
         'ID':                            { 'fieldname': 'Identifier'},
         'Type':                          { 'fieldname': 'Image Type'},
         'Image.ProductQuality':          { 'fieldname': 'Image Product Quality'},
        # 3.3 Observation Metadata         
         'Facility':                      { 'fieldname': 'Facility',  'func': strings2list},
         'Instrument':                    { 'fieldname': 'Instrument','func': strings2list},
         'Spectral.ColorAssignment':      { 'fieldname': 'Color Assignments','func': strings2list},
         'Spectral.Band':                 { 'fieldname': 'Spectral Band','func': strings2list},
         'Spectral.Bandpass':             { 'fieldname': 'BandPass ID',  'func': strings2list},
         'Spectral.CentralWavelength':    { 'fieldname': 'BandPass RefValue','func': strings2list},
         'Spectral.Notes':                { 'fieldname': 'Spectral Notes'},
         'Temporal.StartTime':            { 'fieldname': 'Exposure Start Times','func': strings2list},
         'Temporal.IntegrationTime':      { 'fieldname': 'Exposure Times','func': strings2list},
         'DatasetID':                     { 'fieldname': 'Dataset IDs',  'func': strings2list},
        # 3.4 Coordinate Metadata
         'Spatial.CoordinateFrame':       { 'fieldname': 'Ref Frame'},
         'Spatial.Equinox':               { 'fieldname': 'Equinox'},
          # TODO: Decide which json-fields to use
         'Spatial.ReferenceValue':        { 'fieldname': 'Spatial Reference Value'}, # or 'Spatial.ReferenceValue':{ 'fieldname': ['Dec (J2000)','RA (J2000)']},   # Spatial Reference Values seems to match better with the AVM guid
         'Spatial.ReferenceDimension':    { 'fieldname': 'Spatial Reference Dimension'},
         'Spatial.ReferencePixel':        { 'fieldname': 'Spatial Reference Pixel'},
         'Spatial.Scale':                 { 'fieldname': 'Image Scale', 'func': lambda x: [ s.strip() for s in x.split(',') ]},    # 1.3877e-05, 1.3877037e-05
         'Spatial.Rotation':              { 'fieldname': 'Spatial Rotation'},
         'Spatial.CoordsystemProjection': { 'fieldname': 'Coord Proj'},
         'Spatial.Quality':               { 'fieldname': 'Spatial Quality'},
         'Spatial.Notes':                 { 'fieldname': 'Spatial Notes'},
         'Spatial.FITSHeader':            { 'fieldname': 'SpatialFITSHeader'},
         'Spatial.CDMatrix':              { 'fieldname': 'CD matrix'},                                  # AVM 1.1 (depreciated) 
        # 3.5 Publixher Metadata
         'Publisher':                     { 'fieldname': 'Publisher'},
         'PublisherID':                   { 'fieldname': 'Publisher ID'},
         'ResourceID':                    { 'fieldname': 'Resource ID'},   
         'ResourceURL':                   { 'fieldname': 'URL'},    
         'RelatedResources':              { 'fieldname': 'Related Resouuces'},                          # ['Related Resources','Related Resouuces'] in case they fix the typo
         'MetadataDate':                  { 'fieldname': 'Metadata Date'},
         'MetadataVersion':               { 'fieldname': 'Meta Version'},
        # 3.6 File Metadata
         'File.Type':                     { 'fieldname': 'Image Format'},                               #  TODO: image/tiff ==> TIFF
         'File.Dimension':                { 'fieldname': '', 'func': lambda fieldname: [ jsondict['Image Length'], jsondict['Image Width'] ]},         
         'File.Size':                     { 'fieldname': 'File Size'},        
         'File.BitDepth':                 { 'fieldname': 'Bit Depth'}, 
        # X in AVM 1.1 not defined      
         'X.IngestDate':                  { 'fieldname': 'Ingest Date'},
         'X.ProposalID':                  { 'fieldname': 'Proposal ID'},                                #=> List
         'X.ImageScale':                  { 'fieldname': 'Image Scale', 'func': lambda x: [ s.strip() for s in x.split(',') ]},       
         'X.ImageCount':                  { 'fieldname': 'Image Count'},      
         'X.Source':                      { 'fieldname': 'Source'},        
   }

        
    avmdata = {}
    try:
        # create an avmdict using the values of the jsondict
        for key in mapping.keys():
            json_fieldname = mapping[key]['fieldname']
            value = None
            if json_fieldname in jsondict: value = jsondict[json_fieldname]
            if 'func' in mapping[key]:
                    func = mapping[key]['func']
                    if callable(func):
                        value = func( value )
                    else:
                        logger.error("function %s to process JSON field %s not callable" % (str(func), str(key)))
            elif json_fieldname in jsondict: 
                value = jsondict[json_fieldname]
            avmdata.update( { key: value })

        
                
    except IOError: #Exception:
        avmdata = None
        logger.error("jsondict = %s" % str(jsondict))
        logger.error("invalid jsondict, return None")    
    return avmdata

                         



