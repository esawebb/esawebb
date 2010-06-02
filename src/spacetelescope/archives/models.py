# Spacetelescope.org
# Copyright 2007-2010 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from datetime import date
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
	
	
	name = models.CharField( max_length = 255, blank = True )
	city = models.CharField( max_length = 255, blank = True )
	country = models.CharField( max_length = 255, blank = True )
	age = models.PositiveSmallIntegerField( blank = True )

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

class PressKit (archives.ArchiveModel, StandardArchiveInfo, PhysicalInfo, PrintInfo):
	
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







#class Announcement( archives.ArchiveModel, models.Model ):	
#	id = archives.IdField( )
#	""" """
#
#	title = archives.TitleField( )
#	""" """
#
#	description = archives.DescriptionField( )
#	""" """
#	
#	contacts = models.TextField( blank=True, help_text=_(u'Contacts') )
#	""" """
#	
#	links = models.TextField( blank=True, help_text=_(u'Links') )
#	""" """
#	
#	class Archive:
#		original = archives.ImageResourceManager( type=types.OriginalImageType )
#		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
#		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
#		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
#		wallpaperthumbs = archives.ImageResourceManager( derived='original', type=types.WallpaperThumbnailType )
#		newsfeature = archives.ImageResourceManager( derived='news', type=types.JpegType )
#		news = archives.ImageResourceManager( derived='original', type=types.NewsJpegType )
#		newsmini = archives.ImageResourceManager( derived='news', type=types.NewsMiniJpegType )
#		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
#			   
#		class Meta:
#			root = archive_settings.ANNOUNCEMENT_ROOT
#			release_date = True
#			embargo_date = True
#			last_modified = True
#			created = True
#			published = True
#
#	@staticmethod
#	def get_latest_announcement( len=1 ):
#		qs = Announcement.objects.filter( release_date__lte=datetime.now(), published=True ).order_by( '-release_date' )[:len]
#		return qs
#	
#	class Meta:
#		ordering = ['-release_date','-id']
#		#get_latest_by = "release_date"
#
#	@permalink
#	def get_absolute_url(self):
#		return ('announcements_detail', [str(self.id)])
#	
#	def __unicode__(self):
#		return "%s: %s" % (self.id, self.title)  


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

class Logo( archives.ArchiveModel, StandardArchiveInfo ):	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		   
		eps = archives.ResourceManager(type = types.EpsType)
		illustrator = archives.ResourceManager( type=types.IllustratorType )
		transparent = archives.ResourceManager( type=ImageFileType, verbose_name=_('Transparent PNG') )
		
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


class OnlineArtAuthor (archives.ArchiveModel, StandardArchiveInfo ):
	title = None # Overwrite inherited field

	name = models.CharField( max_length = 255, blank = True )
	city = models.CharField( max_length = 255, blank = True )
	country = models.CharField( max_length = 255, blank = True )
	email = models.CharField( max_length = 255, blank = True )
	link = models.CharField( max_length = 255, blank = True )


	class Meta:
		verbose_name = 'Space Artist'

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
	artist = models.ForeignKey(OnlineArtAuthor)
	credit = None # Overwrite inherited website.
	
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
		verbose_name = 'Space Art'
		verbose_name_plural = 'Space Art' 

	@permalink
	def get_absolute_url(self):
		return ('art_detail', [str(self.id)])
	

#TODO Print Layout? Resources
# Release Resource
#class PrintLayout (archives.ArchiveModel, StandardArchiveInfo, ):
#	
#	class Archive:
#		original = archives.ImageResourceManager( type=types.OriginalImageType )
#		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
#		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
#		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
#		
#		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
#		newsmini = archives.ImageResourceManager( derived='original', type=types.NewsMiniJpegType )
#			   
#		class Meta:
#			root = archive_settings.PRINT_LAYOUT_ROOT
#			release_date = True
#			embargo_date = True
#			last_modified = True
#			created = True
#			published = True  
#			
#	@permalink
#	def get_absolute_url(self):
#		return ('printlayouts_detail', [str(self.id)])

class SlideShow (archives.ArchiveModel, StandardArchiveInfo,ScreenInfo):
	
	class Archive:
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		flash = archives.ResourceManager( type=types.SwfType )
		#flash_dir = archives.ResourceManager( type=types.DirHtmlType, verbose_name= )
					
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
	name = models.CharField( max_length = 255, blank=True )
	country = models.CharField( max_length = 255, blank=True )
	city = models.CharField( max_length = 255, blank=True )
	
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
	   
	class Meta:
		verbose_name = _('FITS Liberator Image')


class UserVideo (archives.ArchiveModel, StandardArchiveInfo, ):
	duration = metadatafields.AVMFileDuration()
	name = models.CharField( max_length = 255, blank=True )
	country = models.CharField( max_length = 255, blank=True )
	city = models.CharField( max_length = 255, blank=True )
	email = models.CharField( max_length = 255, blank = True )
	link = models.CharField( max_length = 255, blank = True )
	
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		thumb = archives.ImageResourceManager( type=types.ThumbnailJpegType )
		videoframe = archives.ImageResourceManager( type=types.JpegType )
		
		mov_small = archives.ResourceManager( type=types.MovType, verbose_name=_(u"Small QT") )
		mov_medium = archives.ResourceManager( type=types.MovType, verbose_name=_(u"Medium QT") )
		mpg_small = archives.ResourceManager( type=types.MpegType, verbose_name=_(u"Small MPEG") )
		mpg_medium = archives.ResourceManager( type=types.MpegType, verbose_name=_(u"Medium MPEG") )
		h264 = archives.ResourceManager( type=types.H264Type, verbose_name=_(u"Large MPEG") )
		broadcast = archives.ResourceManager( type=types.ZipType, verbose_name=_(u"Broadcast") )
		
			   
		class Meta:
			root = archive_settings.USER_VIDEO_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  
		
	@permalink
	def get_absolute_url(self):
		return ('uservideos_detail', [str(self.id)])
	   
	class Meta:
		verbose_name = _('User Video')
		
		
	
class Presentation( archives.ArchiveModel, StandardArchiveInfo ):
	class Archive:
		original = archives.ImageResourceManager( type=types.OriginalImageType )
		large = archives.ImageResourceManager( derived='original', verbose_name=_('Large JPEG'), type=types.JpegType )
		medium = archives.ImageResourceManager( derived='original', type=types.MediumJpegType )
		screen = archives.ImageResourceManager( derived='original', type=types.ScreensizeJpegType )
		thumb = archives.ImageResourceManager( derived='original', type=types.ThumbnailJpegType )
		
		pdf = archives.ResourceManager( type=types.PDFType, verbose_name=_('PDF Presentation') )
		ppt = archives.ResourceManager( type=types.PowerpointPresentationType )
		pps = archives.ResourceManager( type=types.PowerpointSlideshowType )
		   
		class Meta:
			root = archive_settings.PRESENTATION_ROOT
			release_date = True
			embargo_date = True
			last_modified = True
			created = True
			published = True  

	@permalink
	def get_absolute_url(self):
		return ('presentations_detail', [str(self.id)])
