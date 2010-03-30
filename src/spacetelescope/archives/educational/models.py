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

class EducationalMaterial (archives.ArchiveModel, StandardArchiveInfo, PrintInfo, PhysicalInfo, ShopInfo):
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
            
        class Meta:
            root = archive_settings.EDUMATERIAL_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True 

    @permalink
    def get_absolute_url(self):
        return ('education_detail', [str(self.id)])

#class KidsDrawingAuthor( ExtendedContact ):
#    
#    age = models.PositiveSmallIntegerField(blank=True)
#    
#    class Meta:
#        verbose_name = _(u'Kids Drawing Author')            

            
class KidsDrawing (archives.ArchiveModel,StandardArchiveInfo, ):
    
    
    # Didn't find any topic entry in csv file, but column was there
    # topic = None
    
    #author = models.ForeignKey( KidsDrawingAuthor )
    author_name = models.CharField (max_length=255,blank=True)
    author_city = models.CharField (max_length=255,blank=True)
    author_age = models.PositiveSmallIntegerField (blank=True)

    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
               
        class Meta:
            root = archive_settings.KIDS_DRAWING_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
            

    class Meta:
        verbose_name = _(u'Kids Drawing')
 

    @permalink
    def get_absolute_url(self):
            return ('drawings_detail', [str(self.id)])
    
          