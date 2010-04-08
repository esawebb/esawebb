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
from spacetelescope.archives import archive_settings

"""
Base archive definitions across all Spacetelescope archives.

"""

#TODO: rename_ dependencies!!!!

class StandardArchiveInfo ( models.Model ):
    """ 
    Abstract class containing fields shared across all archives 
    
    """
    id = archives.IdField( )
    """ """

    title = archives.TitleField( )
    """ """

    description = archives.DescriptionField( )
    """ """
    
    priority = archives.PriorityField( default = 0)
    """ """
    
    credit = metadatafields.AVMCreditField( )
    """ """

    old_ids = models.CharField(verbose_name=_("Old Ids"), 
                               max_length=50,blank=True, 
                               help_text=_(u'For backwards compatibility: Historic ids of this archive item.') )
    """ """
   
    
    class Meta:
        abstract = True
        ordering = ['-priority','last_modified']
        # TODO: sort by prio for all models?
    
    
    # necessary because ArchiveClass complains!
    class Archive:
        class Meta:
            pass
    
    def __unicode__( self ):
        return self.id



class PhysicalInfo ( models.Model ):
    """ 
    Abstract class containing fields shared across all archives of
    physical objects e.g. Brochures, posters, merchandise etc. 
    """
    
    def _dimensions (self):
        """
        prints dimensions in a nice string 
        """
        if self.width and self.height:
            return '%s cm x %s cm' % (self.width,self.height)    
        elif self.width:
            return '%s cm ' % (self.width)    
        elif self.height:
            return '%s cm ' % (self.height)
        else:
            return ''  
    width = models.CharField (blank=True, max_length=10, help_text = _(u'(cm)') )

    height = models.CharField (blank=True, max_length=10, help_text = _(u'(cm)') )

    size = property( _dimensions )

    weight = models.CharField (blank=True, max_length=10, help_text = _(u'(g)') )
    
    class Meta:
        abstract = True

class PrintInfo ( models.Model ):
    """ 
    Abstract class containing fields shared across all archives of
    print products
    """
    
    pages = models.PositiveSmallIntegerField ( blank=True, help_text=_(u'Number of pages') , null=True)

    class Meta:
        abstract = True

class ScreenInfo ( models.Model ):
    """ 
    Abstract class containing fields shared across all archives of
    screen products (e.g. resolution, x_res, y_res)
    """  
    
    resolution = models.IntegerField ( blank=True, help_text=_(u'Resolution (DPI)'), default = 0 )

    x_size = models.IntegerField ( blank=True, help_text=_(u'X size (px)') )

    y_size = models.IntegerField ( blank=True, help_text=_(u'Y size (px)') )
    
    class Meta:
        abstract = True

class ShopInfo ( models.Model ):
    """ 
    Abstract class containing shop-related information across all archives
    """
        
    sale = models.BooleanField (blank =True , help_text=_(u'Is item on sale?') )
    
    price = models.CharField ( blank = True, max_length=10, help_text=_(u'Price (Eur)'))
    
    delivery = models.CharField ( blank = True, max_length=10, help_text=_(u'Delivery costs (Eur)'))

    class Meta:
        abstract = True
    



