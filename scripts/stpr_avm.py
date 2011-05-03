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

json = "    'BandPass ID'
    ''
    'CD matrix'
    'Dec (J2000)'
    'Equinox'
    'Exposure Start Times'
    'Exposure Times'
    'File Size'
    'Identifier'
    'Image Format'
    'Image Length'
    'Image Scale'
    'Image Width'
    'Ingest Date'
    'Press Release Images'
    'Proposal ID'
    'RA (J2000)'
    'Ref Frame'
   ? 'Related Resources'

"

mapping = {
    'JSON': 'Contact.Address',
    'JSON': 'Contact.City',
    'JSON': 'Contact.Country',
    'Contact Email': 'Contact.Email',
    'JSON': 'Contact.Name',
    'JSON': 'Contact.PostalCode',
    'JSON': 'Contact.StateProvince',
    'JSON': 'Contact.Telephone',
    'JSON': 'Content',
    'JSON': 'Coordinate',
    'JSON': 'Creator',
    'CreatorURL': 'CreatorURL',
    'Credit': 'Credit',
    'Dataset IDs': 'DatasetID',
    'Date Created': 'Date',
    'Description': 'Description',
    'Distance': 'Distance',
    'Distance Notes': 'Distance.Notes',
    'Facility': 'Facility',
    'Headline': 'Headline',
    'JSON': 'Image.ProductQuality',
    'Instrument': 'Instrument',
    'JSON': 'Metadata',
    'Metadata Date': 'MetadataDate',
    'Meta Version': 'MetadataVersion',
    'JSON': 'Observation',
    'JSON': 'Publisher',
    'Publisher ID': 'PublisherID',
    'JSON': 'ReferenceURL',
    'Resource ID': 'ResourceID',
    'URL': 'ResourceURL',
    'Usage Terms': 'Rights',
    'JSON': 'Serialization',
    'Ref Frame': 'Spatial.CoordinateFrame',
    'Coord Proj': 'Spatial.CoordsystemProjection',
    'JSON': 'Spatial.Equinox',
    'Spatial Notes': 'Spatial.Notes',
    'JSON': 'Spatial.Quality',
    'Spatial Reference Dimension': 'Spatial.ReferenceDimension',
    'Spatial Reference Pixel': 'Spatial.ReferencePixel',
    'Spatial Reference Value': 'Spatial.ReferenceValue',
    'Spatial Rotation': 'Spatial.Rotation',
    'JSON': 'Spatial.Scale',
    'Spectral Band': 'Spectral.Band',
    'BandPass ID': 'Spectral.Bandpass',
    'BandPass RefValue': 'Spectral.CentralWavelength',
    'Color Assignments': 'Spectral.ColorAssignment',
    'Spectral Notes': 'Spectral.Notes',
    'Subject Category': 'Subject.Category',
    'Subject': 'Subject.Name',
    'JSON': 'Syntax',
    'JSON': 'Temporal.IntegrationTime',
    'JSON': 'Temporal.StartTime',
    'Title': 'Title',
    'JSON': 'Type'
}




def list_eso_fields():
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
    
#    list_eso_fields()
#    exit()

    
    data = {}
    try:
        fp = open(json_file,'r')
        json_data = json.load(fp)
        fp.close()
    except IOError, (errno, strerror):
        print json_file
        print "I/O error(%s): %s" % (errno, strerror)
    else:
        # convert json_data to a dict of dicts with the st identifier as key:
        for item in json_data:
            data[item['Identifier']] = item
        
        pprint.pprint( data['STScI-PRC-2008-02-d'] )
        ks =  data['STScI-PRC-2008-02-d'].keys()
        ks.sort()
        for k in ks: print "    '%s'" % k
        

                         

'''
    def serialize( self, image, related_cache=None ):
        """
        Serialize image object
        """
        data = {}
        
        def cached_objects( qs, key ):
            if related_cache and key in related_cache:
                return [obj for (pk, obj) in related_cache[key] if pk == image.id]
            else:
                return qs

        def field_to_python( obj, attr ):
            return obj.__class__._meta._name_map[attr][0].from_internal( getattr( obj, attr ) )
        
        def include_related( objs, mapping ):
            d = {}
            for obj in objs:
                for field, tag in mapping.items():
                    try:
                        val = d[tag]
                    except KeyError:
                        val = []
                    
                    attrval = getattr( obj, field )
                    if callable( attrval ): 
                        attrval = attrval()
                    
                    val.append( attrval )
                    d[tag] = val
                    
            return d
        
        #
        # Creator Metadata
        #
        data.update( { 'Creator': image.creator } )
        data.update( { 'CreatorURL': image.creator_url } )
        data.update( 
                    include_related( cached_objects( image.imagecontact_set.all(), 'imagecontact_set' ), 
                    { 'contact_name' :  'Contact.Name', 
                      'contact_email' : 'Contact.Email', 
                      'contact_telephone' : 'Contact.Telephone' 
                    } ) )
        data.update( { 'Contact.Address': prepare_str( image.contact_address ) } )
        data.update( { 'Contact.City': prepare_str( image.contact_city ) } )
        data.update( { 'Contact.StateProvince': prepare_str( image.contact_state_province ) } )
        data.update( { 'Contact.PostalCode': prepare_str( image.contact_postal_code ) } )
        data.update( { 'Contact.Country': prepare_str( image.contact_country) } )
        data.update( { 'Rights': prepare_str(image.rights) } )
        
        #
        # Content Metadata
        #
        data.update( { 'Title': prepare_str( image.title ) } )
        data.update( { 'Headline': prepare_str( image.headline ) } )
        data.update( { 'Description': prepare_str( image.description, html=True ) } )
        data.update( include_related( cached_objects( image.subject_category.exclude( top_level='X' ), 'subject_category' ), { 'avm_code' : 'Subject.Category' } ) )
        data.update( include_related( cached_objects( image.subject_name.all(), 'subject_name'), { 'name' : 'Subject.Name' } ) )
        data.update( { 'Distance': field_to_python( image, 'distance' ) } )
        data.update( { 'Distance.Notes': prepare_str( image.distance_notes ) } )
        data.update( { 'ReferenceURL': image.reference_url } )
        data.update( { 'Credit': prepare_str( image.credit, html=True ) } )
        data.update( { 'Date': image.release_date } )
        data.update( { 'ID': image.id } )
        data.update( { 'Type': image.type } )
        #serializer.add( { 'Image.ProductQuality': image.image_productquality } )
        
        #
        # Observation Metadata
        #
        data.update( include_related(
                cached_objects( image.imageexposure_set.all(), 'imageexposure_set' ), 
                { 
                    'facility' : 'Facility',
                    'instrument' : 'Instrument', 
                    'spectral_color_assignment' : 'Spectral.ColorAssignment', 
                    'spectral_band' : 'Spectral.Band', 
                    'spectral_bandpass' : 'Spectral.Bandpass', 
                    'spectral_central_wavelength' : 'Spectral.CentralWavelength', 
                    'temporal_start_time' : 'Temporal.StartTime', 
                    'temporal_integration_time' : 'Temporal.IntegrationTime', 
                    'dataset_id' : 'DatasetID',  
                } 
            ) )

        data.update( { 'Spectral.Notes': prepare_str( image.spectral_notes ) } )
        
        #
        # Coordinate Metadata
        #
        data.update( { 'Spatial.CoordinateFrame': image.spatial_coordinate_frame } )
        data.update( { 'Spatial.Equinox': image.spatial_equinox } )
        data.update( { 'Spatial.ReferenceValue': field_to_python( image, 'spatial_reference_value' ) } )
        data.update( { 'Spatial.ReferenceDimension': field_to_python( image, 'spatial_reference_dimension' ) } )
        data.update( { 'Spatial.ReferencePixel': field_to_python( image, 'spatial_reference_pixel' ) } )
        data.update( { 'Spatial.Scale': field_to_python( image, 'spatial_scale' ) } )
        data.update( { 'Spatial.Rotation': image.spatial_rotation } )
        data.update( { 'Spatial.CoordsystemProjection': image.spatial_coordsystem_projection } )
        data.update( { 'Spatial.Quality': image.spatial_quality } )
        data.update( { 'Spatial.Notes': prepare_str( image.spatial_notes ) } )
        
        #
        # Publisher Metadata
        #
        data.update( { 'Publisher': image.publisher } )
        #serializer.add( { 'PublisherID': image.publisher_id } ) # Syntax not yet decided upon
        #serializer.add( { 'ResourceID': image.resource_id } )
        #serializer.add( { 'ResourceURL': image.resource_url } )
        data.update( { 'MetadataDate': image.metadata_date } )
        data.update( { 'MetadataVersion': image.metadata_version } )
        
        return Serialization( data ) 
'''

