# Spacetelescope.org
# Copyright 2007-2010 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save, pre_delete, pre_save, \
	post_delete
from django.utils.translation import ugettext as _
from djangoplicity import archives
from djangoplicity.archives.contrib import types
from djangoplicity.archives.contrib.satchmo.models import ShopModel
from djangoplicity.archives.resources import ImageFileType
from djangoplicity.metadata.archives import fields as metadatafields
from djangoplicity.metadata.models import ExtendedContact, Contact, \
	TaxonomyHierarchy, SubjectName
from product.models import Product
from spacetelescope.archives.base import *




class EducationalMaterial (archives.ArchiveModel, StandardArchiveInfo, PrintInfo, PhysicalInfo, ShopModel):
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
			
		pdf = archives.ResourceManager( type=types.PDFType )
		pdfsm = archives.ResourceManager( type=types.PDFType )
			
		
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
	   
	def _get_subtype(self):
		return 'EducationalMaterial'
	
post_save.connect( EducationalMaterial.post_save_handler, sender = EducationalMaterial )
post_delete.connect( EducationalMaterial.post_delete_handler, sender = EducationalMaterial )

#class KidsDrawingAuthor( ExtendedContact ):
#	
#	age = models.PositiveSmallIntegerField(blank=True)
#	
#	class Meta:
#		verbose_name = _(u'Kids Drawing Author')			

			
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
	





"""
Archive for the shop section of ST.org
"""
# =============================================================
# DVDs/CDs
# =============================================================
class CDROM(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopModel):
	
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
			
	class Meta:
		verbose_name = _("DVD/CD")
		verbose_name_plural = _("DVD/CDs")	  
			
	@permalink
	def get_absolute_url(self):
		return ('cdroms_detail', [str(self.id)])	
	
	def _get_subtype(self):
		return 'CDROM'
	
post_save.connect( CDROM.post_save_handler, sender = CDROM )
post_delete.connect( CDROM.post_delete_handler, sender = CDROM )

# =============================================================
# Books
# =============================================================
class Book( archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, PrintInfo, ShopModel ):
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
	
post_save.connect( Book.post_save_handler, sender = Book )
post_delete.connect( Book.post_delete_handler, sender = Book )

# =============================================================
# Brochures
# =============================================================
class Brochure(archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, PrintInfo, ShopModel ):
	
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
	
	def _get_subtype(self):
		return 'Brochure'
	
post_save.connect( Brochure.post_save_handler, sender = Brochure )
post_delete.connect( Brochure.post_delete_handler, sender = Brochure )
	
# =============================================================
# Merchandise
# =============================================================
class Merchandise ( archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopModel ):
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

	def _get_subtype(self):
		return 'Merchandise'
	
	class Meta:
		verbose_name_plural = _('Merchandise')
	
post_save.connect( Merchandise.post_save_handler, sender = Merchandise )
post_delete.connect( Merchandise.post_delete_handler, sender = Merchandise )
				

# =============================================================
# Newsletters and Journals
# =============================================================			
class Newsletter ( archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, PrintInfo, ShopModel ):

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

	def _get_subtype(self):
		return 'Newsletter'
	
post_save.connect( Newsletter.post_save_handler, sender = Newsletter )
post_delete.connect( Newsletter.post_delete_handler, sender = Newsletter )
			
# =============================================================
# Postcards
# =============================================================					   
class PostCard (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopModel ):
	
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

	def _get_subtype(self):
		return 'PostCard'
	
	class Meta:
		verbose_name = _('Postcard')
	
post_save.connect( PostCard.post_save_handler, sender = PostCard )
post_delete.connect( PostCard.post_delete_handler, sender = PostCard )	

# =============================================================
# Posters
# =============================================================
class Poster( archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ScreenInfo, ShopModel ):
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
	
	def _get_subtype(self):
		return 'Poster'
	
post_save.connect( Poster.post_save_handler, sender = Poster )
post_delete.connect( Poster.post_delete_handler, sender = Poster )

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
	

# =============================================================
# Stickers
# =============================================================
class Sticker ( archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, ShopModel ):
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
	
	def _get_subtype(self):
		return 'Sticker'
	
post_save.connect( Sticker.post_save_handler, sender = Sticker )
post_delete.connect( Sticker.post_delete_handler, sender = Sticker )	







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

# =============================================================
# Technical Documents
# =============================================================		   
class TechnicalDocument (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, PrintInfo, ShopModel ):
	
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
	   
	def _get_subtype(self):
		return 'TechnicalDocument'
	
post_save.connect( TechnicalDocument.post_save_handler, sender = TechnicalDocument )
post_delete.connect( TechnicalDocument.post_delete_handler, sender = TechnicalDocument )