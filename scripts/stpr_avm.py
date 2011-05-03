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
# '' for the empty fields, no corresponding stsci-field could be found

mapping = {
    '': 'Contact.Address',
    '': 'Contact.City',
    '': 'Contact.Country',
    'Contact Email': 'Contact.Email',
    '': 'Contact.Name',
    '': 'Contact.PostalCode',
    '': 'Contact.StateProvince',
    '': 'Contact.Telephone',
    '': 'Content',
    '': 'Coordinate',
    '': 'Creator',
    'CreatorURL': 'CreatorURL',
    'Credit': 'Credit',
    'Dataset IDs': 'DatasetID',
    'Date Created': 'Date',
    'Description': 'Description',
    'Distance': 'Distance',
    'Distance Notes': 'Distance.Notes',
    'Facility': 'Facility',
    'Headline': 'Headline',
    '': 'Image.ProductQuality',
    'Identifier' : 'ID',
    'Instrument': 'Instrument',
    '': 'Metadata',
    'Metadata Date': 'MetadataDate',
    'Meta Version': 'MetadataVersion',
    '': 'Observation',
    '': 'Publisher',
    'Publisher ID': 'PublisherID',
    '': 'ReferenceURL',
    'Resource ID': 'ResourceID',
    'URL': 'ResourceURL',                     #?
    'Usage Terms': 'Rights',
    '': 'Serialization',
    'Ref Frame': 'Spatial.CoordinateFrame',   #?
    'Coord Proj': 'Spatial.CoordsystemProjection',
    'Equinox': 'Spatial.Equinox',
    'Spatial Notes': 'Spatial.Notes',
    '': 'Spatial.Quality',
    'Spatial Reference Dimension': 'Spatial.ReferenceDimension',
    'Spatial Reference Pixel': 'Spatial.ReferencePixel',
    'Spatial Reference Value': 'Spatial.ReferenceValue',
    'Spatial Rotation': 'Spatial.Rotation',
    '': 'Spatial.Scale',
    'Spectral Band': 'Spectral.Band',
    'BandPass ID': 'Spectral.Bandpass',
    'BandPass RefValue': 'Spectral.CentralWavelength',
    'Color Assignments': 'Spectral.ColorAssignment',
    'Spectral Notes': 'Spectral.Notes',
    'Subject Category': 'Subject.Category',
    'Subject': 'Subject.Name',
    '': 'Syntax',
    'Exposure Times': 'Temporal.IntegrationTime',
    'Exposure Start Times': 'Temporal.StartTime',
    'Title': 'Title',
    '': 'Type',
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

def list_eso_fields():
    """
    helper function to generate code for the field-mapping dictionary
    """
    script_path = os.path.dirname(sys.argv[0])
    eso_fields = os.path.join(script_path, 'eso_fields.txt')
    pat = re.compile(r'[A-Z]{1}[a-z.]+[A-Za-z]+')
    f = open ( eso_fields )
    fc = ''
    names = set()
    for l in f.readlines(): 
        results = pat.findall(l)    
        for r in results:
            names.add(r)
    
    list = []
    for n in names:
        list.append(n)
    list.sort()
    print "{"
    for l in list:
        print "    'JSON': '%s'," % l
    print "}"
    return


if __name__ == '__main__':
    script_path = os.path.dirname(sys.argv[0])
    json_file = os.path.join(script_path, 'stpr_search.json')
    
    data = load_json(json_file)

    for d in data.keys():
        print "%-25s %-85s %s" % (d, data[d]['Title'], data[d]['Spectral.ColorAssignment'])
        #pprint.pprint( data[d] )
        

                         



