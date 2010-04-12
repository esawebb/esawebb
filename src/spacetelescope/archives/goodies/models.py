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
from datetime import date
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
Archive for the Goodies section of ST
"""

MONTHS_CHOICES = (
                  (1,'January'),
                  (2,'February'),
                  (3,'March'),
                  (4,'April'),
                  (5,'May'),
                  (6,'June'),
                  (7,'July'),
                  (8,'August'),
                  (9,'September'),
                  (10,'October'),
                  (11,'November'),
                  (12,'December'),
                  )
    

        
class Calendar(archives.ArchiveModel, StandardArchiveInfo):
    
    """
    Calendars have the specificities of year and month attributes
    """
    year = models.CharField ( max_length = 4, blank=False, null=False )
    month = archives.ChoiceField (choices = MONTHS_CHOICES, blank=False )
    
    # remove inherited field
    title = None
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        
        pdf = archives.ResourceManager( type=types.PDFType, verbose_name=_('A3 PDF'))
        pdfsm = archives.ResourceManager( type=types.PDFType, verbose_name=_('A4 PDF') )   
        #pdf = archives.ResourceManager( type=types.PDFType, verbose_name=_('A3 PDF (Whole Year)'))
        
        
        class Meta:
            root = archive_settings.CALENDAR_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
            ordering = ['-year','month']
            
    @permalink
    def get_absolute_url(self):
        return ('calendars_detail', [str(self.id)])
       
    def __unicode__(self):
        return 'Calendar %s %s' % (date(year=1901,month=self.month,day=1).strftime('%b'),self.year)     


class OnlineArtAuthor (archives.ArchiveModel, ExtendedContact):
    id = archives.IdField( )
    
    description = archives.DescriptionField( )

    credit = metadatafields.AVMCreditField( )
    """ """
    
    priority = archives.PriorityField( default = 0)
    """ """
    
    credit = metadatafields.AVMCreditField( )

    links = models.TextField()

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        
               
        class Meta:
            root = archive_settings.ONLINE_ART_AUTHOR_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True
            
    def __unicode__(self): 
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('artists_detail', [str(self.id)])
    
class OnlineArt (archives.ArchiveModel, StandardArchiveInfo, ):
    
    artist = models.ForeignKey (OnlineArtAuthor)
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        newsmini = archives.ImageResourceManager( derived='original', type=types.NewsMiniJpegType )
        
               
        class Meta:
            root = archive_settings.ONLINE_ART_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True 
            
    class Meta:
        verbose_name = 'Online Art Piece'
        verbose_name_plural = 'Online Art Pieces' 

    @permalink
    def get_absolute_url(self):
        return ('art_detail', [str(self.id)])
    

#TODO Print Layout? Resources
# Release Resource
#class PrintLayout (archives.ArchiveModel, StandardArchiveInfo, ):
#    
#    class Archive:
#        original = archives.ImageResourceManager( type=types.OriginalImageType )
#        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
#        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
#        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
#        
#        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
#        newsmini = archives.ImageResourceManager( derived='original', type=types.NewsMiniJpegType )
#               
#        class Meta:
#            root = archive_settings.PRINT_LAYOUT_ROOT
#            release_date = True
#            embargo_date = True
#            last_modified = True
#            created = True
#            published = True  
#            
#    @permalink
#    def get_absolute_url(self):
#        return ('printlayouts_detail', [str(self.id)])

class SlideShow (archives.ArchiveModel, StandardArchiveInfo,ScreenInfo):
    
    class Archive:
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        
        flash = archives.ResourceManager( type=types.FlvType)
                    
        class Meta:
            root = archive_settings.SLIDESHOW_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
   
    @permalink
    def get_absolute_url(self):
        return ('slideshows_detail', [str(self.id)])