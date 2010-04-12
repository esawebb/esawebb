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
from djangoplicity.archives.contrib.satchmo.models import ShopModel
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from djangoplicity.metadata.archives import fields as metadatafields  
from djangoplicity.metadata.models import ExtendedContact,Contact, TaxonomyHierarchy, SubjectName

from spacetelescope.archives.base import *

"""
Archive for the shop section of ST.org
"""

class CDROM(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo):
	
	# Didn't find any topic, but key was there
	# topic = None
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		
		zip = archives.ResourceManager( type=types.ZipType )
				
		class Meta:
			root = archive_settings.CDROM_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True	  
			
	@permalink
	def get_absolute_url(self):
		return ('cdroms_detail', [str(self.id)])	
	
from product.models import Product

class Book( archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, PrintInfo, ShopInfo ):
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		
		pdf = archives.ResourceManager( type=types.PDFType )
				
		class Meta:
			root = archive_settings.BOOK_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True	  

	@permalink
	def get_absolute_url(self):
		return ('books_detail', [str(self.id)])
	
	def _get_subtype(self):
		return 'Book'
	
	
#from django.db.models.signals import post_save
#post_save.connect( Book.post_save_handler, sender = Book )
	

class Brochure(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo, PrintInfo):
	
	# Didn't find any topic, but key was there
	# topic = None
		
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		
		pdf = archives.ResourceManager( type=types.PDFType )
		pdfsm = archives.ResourceManager( type=types.PDFType, verbose_name= _('PDF File (Small)') )
		
				
		class Meta:
			root = archive_settings.BROCHURE_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True 
			published = True	  

	@permalink
	def get_absolute_url(self):
		return ('brochures_detail', [str(self.id)])	
	

class Merchandise (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo):
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
				
		class Meta:
			root = archive_settings.MERCHANDISE_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  

	@permalink
	def get_absolute_url(self):
		return ('merchandise_detail', [str(self.id)])	
	

			
class Newsletter (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo, PrintInfo):
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )

		pdf = archives.ResourceManager( type=types.PDFType )
		#Deprecated
		#doc = archives.ResourceManager( type=types.DocType )
		#sciencepaper = archives.ResourceManager( type=types.PDFType )
		#text = archives.ResourceManager( type=types.TxtType )
			 
		class Meta:
			root = archive_settings.NEWSLETTER_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  

	@permalink
	def get_absolute_url(self):
		return ('newsletters_detail', [str(self.id)])	
	

			
					   
class PostCard (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo):
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
			   
		class Meta:
			root = archive_settings.POSTCARD_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  

	@permalink
	def get_absolute_url(self):
		return ('postcards_detail', [str(self.id)])	
	


class Poster(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo):
	
	# TODO: has topic!! set(['hubble'])
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		
		
		class Meta:
			root = archive_settings.POSTER_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True	

	@permalink
	def get_absolute_url(self):
		return ('posters_detail', [str(self.id)])	
	


class PressKit (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo, PrintInfo):
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		
		pdf = archives.ResourceManager( type=types.PDFType )
		
			   
		class Meta:
			root = archive_settings.PRESSKIT_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  

	@permalink
	def get_absolute_url(self):
		return ('presskits_detail', [str(self.id)])	
	

class Sticker (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopInfo):
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
					   
		class Meta:
			root = archive_settings.STICKER_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  

	@permalink
	def get_absolute_url(self):
		return ('stickers_detail', [str(self.id)])	
	


