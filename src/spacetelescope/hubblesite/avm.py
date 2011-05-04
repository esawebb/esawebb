#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#   access avm metadata as dict, source is a json file from
#   http://archdev.stsci.edu/stpr/search.php 
#   
#*************************************************************************************************************

import os, sys
import re
import pprint
import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson as json

def load_json(json_file):
    '''
    loads and returns the content of the given json file as a dictionary of subdictionaries 
    with image identifier as key
    '''
    data = {}
    try:
        fp = open(json_file,'r')
        json_data = json.load(fp)
        fp.close()
    except IOError, (errno, strerror):
        logger.error("I/O error(%s): %s" % (errno, strerror))
        logger.error("file %s not found, return None" % json_file )
        data = None
    else:
        # convert json_data to a dict of dicts with the identifier as key:
        for metadataset in json_data:
            if type(metadataset) != type({}):
                logger.error("type of json metadataset is not a dict %s" % type(metadataset) )
            else:
                data.update( { metadataset['Identifier']: metadataset}  )
    return data

def jsondict2avmdict(jsondict):
    ''' 
    transforms the json data into a dictionary of subdictionaries 
    using the keywords from mapping for the subdictionaries
    '''
    # mapping of the json fields from http://archdev.stsci.edu/stpr/search.php 
    # to names in defined in AVM 1.1 and used in media.models.AVMImageSerializer
    # and if not there, to new names 
    # dict { 'JSON': 'AVM', ....}
    mapping = {
        'Contact Email': 'Contact.Email',
        'CreatorURL': 'CreatorURL',
        'Credit': 'Credit',
        'Dataset IDs': 'DatasetID',
        'Date Created': 'Date',
        'Description': 'Description',
        'Distance': 'Distance',
        'Distance Notes': 'Distance.Notes',
        'Facility': 'Facility',
        'Headline': 'Headline',
        'Identifier' : 'ID',
        'Instrument': 'Instrument',
        'Metadata Date': 'MetadataDate',
        'Meta Version': 'MetadataVersion',
        'Publisher ID': 'PublisherID',
        'Resource ID': 'ResourceID',
        'URL': 'ResourceURL',                     #? ambigous
        'Usage Terms': 'Rights',
        'Ref Frame': 'Spatial.CoordinateFrame',   
        'Coord Proj': 'Spatial.CoordsystemProjection',
        'Equinox': 'Spatial.Equinox',
        'Spatial Notes': 'Spatial.Notes',
        'Spatial Reference Dimension': 'Spatial.ReferenceDimension',
        'Spatial Reference Pixel': 'Spatial.ReferencePixel',
        'Spatial Reference Value': 'Spatial.ReferenceValue',
        'Spatial Rotation': 'Spatial.Rotation',
        'Spectral Band': 'Spectral.Band',
        'BandPass ID': 'Spectral.Bandpass',
        'BandPass RefValue': 'Spectral.CentralWavelength',
        'Color Assignments': 'Spectral.ColorAssignment',
        'Spectral Notes': 'Spectral.Notes',
        'Subject Category': 'Subject.Category',
        'Subject': 'Subject.Name',
        'Exposure Times': 'Temporal.IntegrationTime',
        'Exposure Start Times': 'Temporal.StartTime',
        'Title': 'Title',
        # new fields from json file (http://archdev.stsci.edu), using tag names from avm 1.1 where possible
        'CD matrix'  : 'Spatial.CDMatrix', # AVM 1.1 (depreciated) 
        'Dec (J2000)': 'Spatial.Dec',
        'RA (J2000)' : 'Spatial.RA',
        'File Size'  : 'File.Size',  # AVM 1.1
        'Image Format': 'File.Type', # AVM 1.1   TODO: image/tiff ==> TIFF
        'Image Length': 'Image.Length',
        'Image Scale' : 'Image.Scale',
        'Image Width' : 'Image.Width',
        'Ingest Date' : 'Image.Date',
        'Press Release Images': 'PressReleaseImages',
        'Proposal ID' : 'ProposalID',
        'Related Resouuces' : 'RelatedResources',
        'Related Resources' : 'RelatedResources'     # in case they fix the typo
    }
    data = {}
    
    try:
        # convert jsondict to an avmdict replacing the keys with the above mapping:
        # TODO: process the metadata to make it AVM conform (ie File.Type image/tiff ==> TIFF)
        for key in jsondict.keys():
            # build dict with replaced keys:
            metadataset = jsondict[key]
            newitem = {}
            for key in metadataset.keys():  
                newitem.update( { mapping[key]: metadataset[key] }  )
            data.update( { metadataset['Identifier']: newitem })
    except Exception:
        data = None
        logger.error("jsondict = %s" % str(jsondict))
        logger.error("invalid jsondict, return None")    
    return data



if __name__ == '__main__':
    # for testing
    logging.basicConfig()
    
    script_path = os.path.dirname(sys.argv[0])
    json_file = os.path.join(script_path, 'stpr_search.json')
    
    data = load_json(json_file)
    avm = jsondict2avmdict(data)
    
    pprint.pprint(avm)
    if avm:
        pprint.pprint( avm['STScI-PRC-2010-36-a'] )
        for d in avm.keys():
            print "%-25s %-85s %s" % (d, avm[d]['Title'], avm[d]['Spectral.ColorAssignment'])
            
        
            

                         



