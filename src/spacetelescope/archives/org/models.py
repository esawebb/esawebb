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
from djangoplicity.archives.resources import ImageFileType
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from djangoplicity.metadata.archives import fields as metadatafields  
from djangoplicity.metadata.models import ExtendedContact,Contact, TaxonomyHierarchy, SubjectName

from spacetelescope.archives.base import *

"""
Archive for the organizational section of ST (about us)
"""

class Announcement (archives.ArchiveModel,StandardArchiveInfo,):

    links = models.TextField( blank=True, help_text=_(u'Associated Links') )
    """ """
    
    contacts = models.TextField( blank=True, help_text=_(u'Associated Contacts') )
    """ """

    subject_category = metadatafields.AVMSubjectCategoryField()
    """ """
    
    subject_name = metadatafields.AVMSubjectNameField()
    """ """
    
    facility = metadatafields.FacilityManyToManyField()



    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        newsmini = archives.ImageResourceManager( derived='original', type=types.NewsMiniJpegType )
        
               
        class Meta:
            root = archive_settings.ANNOUNCEMENT_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  

    @permalink
    def get_absolute_url(self):
        return ('announcements_detail', [str(self.id)])  


class ConferencePoster(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo,ScreenInfo):
        
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
           
        class Meta:
            root = archive_settings.CONFERENCE_POSTER_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
    
    @permalink
    def get_absolute_url(self):
        return ('conference_posters_detail', [str(self.id)])  

class Logo(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo,ScreenInfo):    
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
           
        eps = archives.ResourceManager(type = types.EpsType)
        illustrator = archives.ResourceManager( type=types.IllustratorType )
        transparent = archives.ResourceManager( type=ImageFileType )
        
        class Meta:
            root = archive_settings.LOGO_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
            
            
    @permalink
    def get_absolute_url(self):
        return ('logos_detail', [str(self.id)])  
            
class TechnicalDocument (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo,PrintInfo):
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
        
        pdf = archives.ResourceManager( type=types.PDFType )
        
               
        class Meta:
            root = archive_settings.TECHDOC_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  

    @permalink
    def get_absolute_url(self):
        return ('techdocs_detail', [str(self.id)])  

