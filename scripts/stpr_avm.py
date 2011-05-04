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
#*************************************************************************************************************

import os, sys
import re
import pprint

from django.utils import simplejson as json

# mapping of the json fields from http://archdev.stsci.edu/stpr/search.php 
# to names in media.models.AVMImageSerializer
# and if not there, to new names 
# dict { 'JSON': 'AVMImageSerializer', ....}

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
    'URL': 'ResourceURL',                     #?
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
    # new fields from json file (http://archdev.stsci.edu) starting with n.      
    'CD matrix'  : 'n.CD.Matrix',
    'Dec (J2000)': 'n.Spatial.Dec',
    'RA (J2000)' : 'n.Spatial.RA',
    'File Size'  : 'n.FileSize',
    'Image Format': 'n.Image.Format',
    'Image Length': 'n.Image.Length',
    'Image Scale' : 'n.Image.Scale',
    'Image Width' : 'n.Image.Width',
    'Ingest Date' : 'n.Image.Date',
    'Press Release Images': 'n.PressReleaseImages',
    'Proposal ID' : 'n.ProposalID',
    'Related Resouuces' : 'n.RelatedResources',
    'Related Resources' : 'n.RelatedResources'     # in case they fix the typo
}


def load_json(json_file):
    '''
    loads the content of the json file into a dictionary using the keywords from mapping for the new dict
    returns the filled dict containing metadata
    '''
    data = {}
    try:
        fp = open(json_file,'r')
        json_data = json.load(fp)
        fp.close()
    except IOError, (errno, strerror):
        print json_file
        print "I/O error(%s): %s" % (errno, strerror)
        print "the script looks for json file here: %s (in the same folder as the script itself, sorry ;-)" % json_file
        return None
    else:
        # convert json_data to a dict of dicts with the identifier as key and using the keys from mapping for the fields:
        for item in json_data:
            # build new dict:
            newitem = {}
            for key in item.keys():
                #newitem[mapping[key]] = item[key]  
                newitem.update( { mapping[key]: item[key] }  )
            data[item['Identifier']] = newitem
    
    return data


if __name__ == '__main__':
    script_path = os.path.dirname(sys.argv[0])
    json_file = os.path.join(script_path, 'stpr_search.json')
    
    data = load_json(json_file)
    if data:
        for d in data.keys():
            print "%-25s %-85s %s" % (d, data[d]['Title'], data[d]['Spectral.ColorAssignment'])
            
        pprint.pprint( data['STScI-PRC-2010-36-a'] )
            

                         



