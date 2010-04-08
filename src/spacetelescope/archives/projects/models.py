# Spacetelescope.org
# Copyright 2007-2010 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from django.db import models 
from django.db.models import permalink
from django.utils.translation import ugettext as _
from django.conf import settings

from djangoplicity import archives
from djangoplicity.archives.contrib import types
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from djangoplicity.metadata.archives import fields as metadatafields  
from djangoplicity.metadata.models import ExtendedContact,Contact, TaxonomyHierarchy, SubjectName

from spacetelescope.archives.base import *

"""
Archive for the projects section of ST.org
"""


class Exhibition (archives.ArchiveModel, StandardArchiveInfo, ):
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
                   
        class Meta:
            root = archive_settings.EXHIBITION_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
            
    @permalink
    def get_absolute_url(self):
        return ('exhibitions_detail', [str(self.id)])   

class FITSImage (archives.ArchiveModel, StandardArchiveInfo, ):

    #TODO convert to metadata model
    country = models.CharField (max_length = 50)
    city = models.CharField (max_length = 50)
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        
               
        class Meta:
            root = archive_settings.FITS_IMAGE_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
        
    @permalink
    def get_absolute_url(self):
        return ('fitsimages_detail', [str(self.id)])   

