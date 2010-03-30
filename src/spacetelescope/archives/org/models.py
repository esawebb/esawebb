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

#TODO: with contacts
#TODO: move this to djangoplicity.releases ?
#TODO: associated with resources. basically an image archive
class Announcement (archives.ArchiveModel,StandardArchiveInfo,):

    # TODO: has topic! set(['', 'Nebula', 'Cosmology'])

    #TODO should this be appended to description? -> Two seperate
    links = models.TextField( blank=True, help_text=_(u'Associated Links') )
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
            

class AnnouncementContact( ExtendedContact ):
    announcement = models.ForeignKey( Announcement )
    
    class Meta:
        verbose_name = _(u'Contact')

class ConferencePoster(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo):
    
    # TODO: has topic!! set(['hubble'])
    
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

class Logo(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo,ScreenInfo):
    # TODO added screeninfo which wasn't originally in Archive
    
    # Didn't find any topic, but key was there
    # topic = None
    
    class Archive:
        original = archives.ImageResourceManager( type=types.OriginalImageType )
        large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
        medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
        screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
        thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
           
        eps = archives.ResourceManager(type = types.EpsType)
        # banner = ### TODO: is empty at the moment
        # businesscard = ### TODO: is empty at the moment
        illustrator = archives.ResourceManager( type=types.IllustratorType )
        transparent = archives.ResourceManager( type=ImageFileType )
        
        class Meta:
            root = archive_settings.LOGO_ROOT
            release_date = True
            embargo_date = True
            last_modified = True
            created = True
            published = True  
            
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



