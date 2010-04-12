# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
import os, shutil
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from django.contrib.redirects.models import Redirect
from djangoplicity.migration import MigrationError
from djangoplicity.migration.apps.archives import CSVDataSource, DataMapping
from djangoplicity.releases.models import Release, ReleaseType
from djangoplicity.releases.models import Image
from spacetelescope.archives.educational.models import *
from spacetelescope.archives.goodies.models import *
from spacetelescope.archives.products.models import *
from spacetelescope.archives.projects.models import *
from spacetelescope.archives.org.models import *

import csv

COPY_INSTEAD_OF_MOVE = True
#for all resources except THUMBS, only touch new ones instead of copy
DEBUG_ONLY_TOUCH = True

csv.register_dialect( 'spacetelescope', delimiter='|' )

class SpacetelescopeCSVDataSource( CSVDataSource ):
	dialect = 'spacetelescope'
	
	def __init__( self, filename ):
		super( SpacetelescopeCSVDataSource, self ).__init__( filename, dialect = self.dialect )
		
		
		
class SpacetelescopeDataMapping( DataMapping ):
	"""
	Base class with helper methods for mapping an spacetelescope.org
	archive into a djangoplicity archive. 
	"""
	BASE = ""
	#ROOT = ""
	#BASE = ""
	
	format_mapping = {}

	OLD_FMT_ROOT = ""
	NEW_FMT_ROOT = ""
	
	def run(self):
		self._create_object()
		self._create_redirect()
		self._move_resources()
		
	def _parse_date( self, text ):
		"""
		Parse a date as used on spacetelescope.org CSV-files
		"""
		if text:
			try:
				return datetime.strptime( text, "%d/%m/%Y %H:%M" )
			except ValueError:
				raise MigrationError( "Couldn't convert date/time string: %s" % text )
		return None
	
	def old_urls(self):
		"""
		Return a list of old URLs where this archive item was accessible.
		"""
		return ["%s/html/%s.html" % (self.BASE, self.obj.id),]
	
	def _create_redirect(self):
		"""
		Setup redirects for the archive item. Can be overwritten in 
		subclass if special redirects are needed. If several old URLs
		needs to be mapped to the one new URL, it's usually enough to 
		overwrite old_urls() instead.
		"""
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r = Redirect( site = self.conf['pages']['site'], old_path=url, new_path=new_url )
			r.save()
			
	def _create_object(self):
		"""
		Creating the archive item object and store it in self.obj.
		Must be overwritten in subclass. 
		"""
		pass
	
	VALID_EXTS = ['.jpg','.gif','.tif','.pdf','.zip','.eps','.ai','.png']
	def _find_old_resource(self, fmt ):
		old_path = os.path.join( self.OLD_FMT_ROOT, fmt )
		
		
		
		#look for files named with self.obj.id in old_path 
		
		p = old_path
		for ext in self.VALID_EXTS:
			old_path = os.path.join(p, self.obj.id + ext)
			if os.path.exists(old_path):
				return old_path
		

	def _move_resources(self,copy=COPY_INSTEAD_OF_MOVE):
		"""
		DEBUG: default copy and not move
		"""
		if copy:
			action = 'Copying'
		else:
			action = 'Moving'
			
		for old_fmt, new_fmt in self.format_mapping.iteritems():
			old_filepath = self._find_old_resource( old_fmt )
			if not old_filepath:
				self.logger.debug("Could not find a suitable %s format for obj %s" % (old_fmt,self.obj.id))
				continue
			#for p in old_filepaths:
			tmp,ext = os.path.splitext(old_filepath)
			filename = os.path.basename( old_filepath ) 
			new_dir = os.path.join( self.NEW_FMT_ROOT, new_fmt )
			if not os.path.exists( new_dir ):
				# create new directory 
				os.makedirs(new_dir)
				
			
			
			new_filepath = os.path.join( new_dir, self.obj.id+ext )
			f,ext = os.path.splitext(new_filepath)
			self.logger.debug( "%s: %s >> %s... [%s]" % (self.obj.id,old_fmt,new_fmt,ext) )
			if DEBUG_ONLY_TOUCH and new_fmt != 'thumb':
			     open(new_filepath, 'w').close() 
			elif copy:
				shutil.copy(old_filepath,new_filepath)
			else:
				pass
			    #os.rename( p, new_filepath )
				

#
# TOOD: Remove HTML tags from title
# TOOD: Format links
# TODO: connect with images + main image
# TODO: fix release_type
# TODO: import contacts
# TODO: extract contacts???

class NewsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/news"
	#format_mapping = {'thumbs':'thumb'}
	
	# handle layouts
	#TODO handle print layouts
	def _move_resources(self,copy=COPY_INSTEAD_OF_MOVE):
		super(SpaceTelescopeDataMapping,self)._move_resources(copy)
		
		
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r = Redirect( site = self.conf['pages']['site'], old_path=url, new_path=new_url )
			r.save()
	
	def _create_object(self):
		# id, releasetype, title
		self.obj = Release( 
				id=self.id(),
				release_type=self.release_type(),
				title=self.title(), 
				headline=self.headline(),
				description=self.description(),
				notes=self.notes(),
				links=self.links(),
				release_date=self.release_date(),
				embargo_date=self.embargo_date(),
			)
		self.obj.save()
	
	def id(self):
		return self.dataentry['id']

	def release_type(self):
		return ReleaseType.objects.get_or_create( name=self.dataentry['release_type'] )[0]
	
	def title(self):
		return self.dataentry['title']
	
	def headline(self):
		soup = BeautifulSoup( self.dataentry['lead'] )
		return unicode( soup )
		
	def description(self):
		soup = BeautifulSoup( self.dataentry['text'] )
		return unicode( soup )
		
	def notes(self):
		soup = BeautifulSoup( self.dataentry['notes'] )
		return unicode( soup )
		
	def links(self):
		soup = BeautifulSoup( self.dataentry['links'] )
		return unicode( soup )
	
	def release_date( self ):
		return self._parse_date( self.dataentry['release date/local time Munich (CET or CEST)'] )
	
	def embargo_date( self ):
		return self._parse_date( self.dataentry['Stage date/local time Munich (CET or CEST)'] )
		

# Lots
class ImagesDataMapping( SpacetelescopeDataMapping ):
	BASE = "/images"
	
	format_mapping = {'thumbs':'thumb'}

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/images/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/images/"
	
	def run(self):
		self._create_object()
		self._create_redirect()
		
	def _create_object(self):
		# id, releasetype, title
		self.obj = Image( 
				id=self.id(),
				priority=0,
				title=self.title(), 
			)
		self.obj.save()
	
	def id(self):
		return self.dataentry['id']

	def title(self):
		soup = BeautifulSoup( self.dataentry['Title'] )
		return unicode( soup )		

# TODO: extract thumb from main image
class NewsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/news"
	
	#format_mapping = {'thumbs':'thumb'}

	#OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/news/"
	#NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/education/"

	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r = Redirect( site = self.conf['pages']['site'], old_path=url, new_path=new_url )
			r.save()
	
	def _create_object(self):
		# id, releasetype, title
		self.obj = Release( 
				id=self.id(),
				release_type=self.release_type(),
				title=self.title(), 
				headline=self.headline(),
				description=self.description(),
				notes=self.notes(),
				links=self.links(),
				release_date=self.release_date(),
				embargo_date=self.embargo_date(),
			)
		self.obj.save()
	
	def id(self):
		return self.dataentry['id']

	def release_type(self):
		return ReleaseType.objects.get_or_create( name=self.dataentry['release_type'] )[0]
	
	def title(self):
		return self.dataentry['title']
	
	def headline(self):
		soup = BeautifulSoup( self.dataentry['lead'] )
		return unicode( soup )
		
	def description(self):
		soup = BeautifulSoup( self.dataentry['text'] )
		return unicode( soup )
		
	def notes(self):
		soup = BeautifulSoup( self.dataentry['notes'] )
		return unicode( soup )
		
	def links(self):
		soup = BeautifulSoup( self.dataentry['links'] )
		return unicode( soup )
	
	def release_date( self ):
		return self._parse_date( self.dataentry['release date/local time Munich (CET or CEST)'] )
	
	def embargo_date( self ):
		return self._parse_date( self.dataentry['Stage date/local time Munich (CET or CEST)'] )
		
		

class EducationalMaterialsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/kidsandteachers/educational"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'highres_pdf':'pdf',
					  'lowres_pdf':'pdfsm',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/kidsandteachers/education/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/education/"
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()

	
	def _create_object(self):
		# id, releasetype, title
		self.obj = EducationalMaterial( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				pages=self.pages(),
				width=self.width(),
				height=self.height(),
				weight=self.weight(),
				priority=self.priority(),
				credit=self.credit(),
				sale=self.sale(),
				price=self.price(),
				delivery=self.delivery(),
			)
		self.obj.save()
		
	
	def id(self):
		return self.dataentry['id']

	def title(self):
		return self.dataentry['Title']
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )

	def pages(self):
		return self.dataentry['Pages']
		
	def width(self):
		return self.dataentry['Width']
		
	def height(self):
		return self.dataentry['Height']

	def weight(self):
		return self.dataentry['Weight']
		
	def priority(self):
		return self.dataentry['priority']
		
	def credit(self):
		return self.dataentry['credit']
		
	def sale(self):
		return self.dataentry['Sale']
		
	def price(self):
		return self.dataentry['Price']
		
	def delivery(self):
		return self.dataentry['Delivery'] if self.dataentry['Delivery'] is not None else ''
		

class KidsDrawingsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/kidsandteachers/drawings"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/kidsandteachers/drawings/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/drawings/"
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()

	
	def _create_object(self):
		# id, releasetype, title
		self.obj = KidsDrawing( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				author_name = self.author_name(),
				author_age = self.author_age(),
				author_city = self.author_city(),
			)
		self.obj.save()
		
	
	def id(self):
		return self.dataentry['id']

	def title(self):
		return self.dataentry['Title']
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )
		
	def priority(self):
		return self.dataentry['priority']
		
	def credit(self):
		return unicode(self.dataentry['credit'].decode('iso-8859-1'))
		
	def author_name(self):
		return unicode(self.dataentry['Name'].decode('iso-8859-1'))
		
	def author_age(self):
		return self.dataentry['Age']

	def author_city(self):
		return unicode(self.dataentry['Town'].decode('iso-8859-1'))



#TODO copy pdf resources ALL to each month/year
class CalendarsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/goodies/calendars"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'medium':'medium',
					  'large':'large',
					  'pdf_a3':'pdf',
					  'pdf_a4':'pdfsm',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/calendar/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/calendars/"
	
	MONTHS = {'January':'01',
			  'February':'02',
			  'March':'03',
			  'April':'04',
			  'May':'05',
			  'June':'06',
			  'July':'07',
			  'August':'08',
			  'September':'09',
			  'October':'10',
			  'November':'11',
			  'December':'12',
			  }
	
	def _find_old_resource(self, fmt ):
		old_path = os.path.join( self.OLD_FMT_ROOT, fmt )
		id = "%s%02d" % (unicode(self.obj.year)[2:],self.obj.month)
		old_path = os.path.join(old_path, id)
		#look for files named with self.obj.id in old_path 
		
		p = old_path
		for ext in self.VALID_EXTS:
			old_path = p+ ext
			print old_path
			if os.path.exists(old_path):
				return old_path	
	
		
		
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()

	
	def _create_object(self):
		# id, releasetype, title
		self.obj = Calendar( 
				id=self.id(),
				year=self.year(),
				month=self.month(),
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
			)
		self.obj.save()
		
	
	def id(self):
		return "cal%s%s" % (self.year(),self.MONTHS[self.dataentry['month']]  )
			
	def year (self):
		return int(self.dataentry['year'])
	
	def month (self):
		return int(self.MONTHS[self.dataentry['month']])
	
	
	def description(self):
		soup = BeautifulSoup( self.dataentry['caption'].decode('iso-8859-1').encode('utf8') )
		return unicode( soup )
		
	def priority(self):
		return 0 # there is no prio in csv
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8')
		
class SlideShowDataMapping( SpacetelescopeDataMapping ):
	BASE = "/goodies/slideshows"
	
	format_mapping = {'thumbs':'thumb',
					  #'flash':'flash',
					  #TODO: handle flash

					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/slideshows/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/slideshows/"
	
	
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()

	
	def _create_object(self):
		# id, releasetype, title
		self.obj = SlideShow( 
				id=self.id(),
				title = self.title(),
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				x_size = self.x_size(),
				y_size = self.y_size(),
			)
		self.obj.save()
		
	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title']
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )
		
	def priority(self):
		return self.dataentry['priority']
		
	def credit(self):
		return unicode(self.dataentry['Credit'])
	
	def x_size (self):
		return self.dataentry['xsize']
	
	def y_size (self):
		return self.dataentry['ysize']
	
	
class ProductDataMapping (SpacetelescopeDataMapping):
	#base data mapping for all products (shop)
	model = None  
	has_pages=False
	format_mapping = {'thumbs':'thumb'}
    
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()

	def _create_object(self):
		# id, releasetype, title
		
		self.obj = self.model( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				width=self.width(),
				height=self.height(),
				weight=self.weight(),
				priority=self.priority(),
				credit=self.credit(),
				sale=self.sale(),
				price=self.price(),
				delivery=self.delivery(),
			)

		if self.has_pages:
			self.obj.pages = self.pages()
		self.obj.save()
		
	def _dataentry(self,key):
		# attempt lowercase retrieve and then title. otherwise fail
		try:
			return self.dataentry[key.lower()]
		except KeyError:
			return self.dataentry[key.title()]
	
	def id(self):
		return self._dataentry('id')
	
	def title(self):
		return self._dataentry('Title').decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self._dataentry('Description').decode('iso-8859-1').encode('utf8') )
		return unicode( soup )
	
	def pages(self):
		if self.has_pages:
			
			return self._dataentry('Pages')
		
		else:
			return None
	def width(self):
		return self._dataentry('Width')
		
	def height(self):
		return self._dataentry('Height')
	
	def weight(self):
		return self._dataentry('Weight')
		
	def priority(self):
		return self._dataentry('priority')
		
	def credit(self):
		return self._dataentry('credit').decode('iso-8859-1').encode('utf8') 
		
	def sale(self):
		return self._dataentry('Sale')
		
	def price(self):
		return self._dataentry('Price')
		
	def delivery(self):
		return self._dataentry('Delivery') if self._dataentry('Delivery') is not None else ''


class CDROMDataMapping(ProductDataMapping):
	model = CDROM
	BASE = "/products/cdroms"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'medium':'medium',
					  'large':'large',
					  'zip':'zip',
					  }
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/cdroms/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/cdroms/"
	
class BookDataMapping(ProductDataMapping):
	model = Book
	BASE = "/products/books"
	format_mapping = {'thumbs':'thumb',
				  'original':'original',
				  'medium':'medium',
				  'large':'large',
				  'screen':'screen',
				  'pdf':'pdf',
				  }
	
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/books/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/books/"
	
class BrochureDataMapping(ProductDataMapping):
	model = Brochure
	BASE = "/products/brochures"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf',
					  'pdfsm':'pdfsm',
					  }
	
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/brochures/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/brochures/"
	
class MerchandiseDataMapping(ProductDataMapping):
	model = Merchandise
	BASE = "/products/merchandise"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/merchandise/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/merchandise/"
	
class NewsletterDataMapping(ProductDataMapping):
	model = Newsletter
	BASE = "/products/newsletters"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf',
					  }
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/newsletters/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/newsletters/"

class PostCardDataMapping(ProductDataMapping):
	model = PostCard
	BASE = "/products/postcards"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/postcards/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/postcards/"

class PosterDataMapping(ProductDataMapping):
	model = Poster
	BASE = "/products/posters"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/posters/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/posters/"

class StickerDataMapping(ProductDataMapping):
	model = Sticker
	BASE = "/products/stickers"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/stickers/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/stickers/"


class PressKitDataMapping(ProductDataMapping):
	model = PressKit
	BASE = "/products/presskits"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf'
					  }
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/presskits/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/presskits/"
	
	
	

# ORG
#TODO copy image resources
class AnnouncementDataMapping (ProductDataMapping):

	BASE = "/updates"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'newsmini':'newsmini',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/updates/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/announcements/"
	
	
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()
	
	
	#def copy_image_resource (self):
		
	
	def _create_object(self):
		self.obj = Announcement( 
				id=self.id(),
				title = self.title(),
				description=self.description(),
				contacts=self.contacts(),
				links = self.links (),
			)
		self.obj.save()
		
		
	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['text'] )
		return unicode( soup )
		
	def contacts(self):
		return BeautifulSoup(self.dataentry['contacts'].decode('iso-8859-1').encode('utf8'))
	
	def links (self):
		soup = BeautifulSoup( self.dataentry['links'] )
		return unicode( soup )
	
class ConferencePosterDataMapping(SpacetelescopeDataMapping):
	BASE = "/about_us/conference_posters"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about_us/conference_posters/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/conference_posters/"

	def _create_object(self):
		
		self.obj = ConferencePoster( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				width=self.width(),
				height=self.height(),
				resolution=self.resolution(),
				priority=self.priority(),
				credit=self.credit(),
				x_size = 0,
				y_size = 0,
				)
		self.obj.save()	

	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )

	def width(self):
		return self.dataentry['width']
		
	def height(self):
		return self.dataentry['height']
	
	def resolution(self):
		return self.dataentry['dpi']
		
	def priority(self):
		return self.dataentry['priority']
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8') 

class LogoDataMapping(SpacetelescopeDataMapping):
	BASE = "/about_us/logos"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'eps':'eps',
					  'illustrator':'illustrator',
					  'transparent':'transparent',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about_us/logos/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/logos/"

	def _create_object(self):
		
		self.obj = Logo( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				x_size =0,
				y_size =0,
				resolution = 0,
				)
		self.obj.save()	

	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )

		
	def priority(self):
		return self.dataentry['priority']
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8') 

class TechnicalDocumentDataMapping(ProductDataMapping):
	model = TechnicalDocument
	BASE = "/about_us/techdocs"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf',
					  }
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/techdocs/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/techdocs/"
	


class ExhibitionDataMapping(SpacetelescopeDataMapping):
	BASE = "/projects/exhibitions/"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/projects/exhibitions/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/exhibitions/"

	def _create_object(self):
		
		self.obj = Exhibition( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				)
		self.obj.save()	

	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )

	def priority(self):
		return self.dataentry['priority']
		
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8') 

class FITSImageDataMapping(SpacetelescopeDataMapping):
	BASE = "/projects/fits_liberator/fitsimages/"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/projects/fits_liberator/fitsimages/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/fitsimages/"

	def _create_object(self):
		
		self.obj = FITSImage( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				city = self.city(),
				country = self.country(),
				)
		self.obj.save()	

	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )

	def city(self):
		return self.dataentry['City'].decode('iso-8859-1').encode('utf8') 

	def country(self):
		return self.dataentry['Country'].decode('iso-8859-1').encode('utf8') 

		
	def priority(self):
		return self.dataentry['priority']
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8') 
	

class OnlineArtAuthorDataMapping(SpacetelescopeDataMapping):
	BASE = "/goodies/art/"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }



	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/art/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/artists/"

	def _create_object(self):
		
		self.obj = OnlineArtAuthor( 
				id=self.id(),
				name=self.name(), 
				description=self.description(),
				city = self.city(),
				country = self.country(),
				email = self.email(),
				links = self.links(),
				priority = self.priority()
				)
		self.obj.save()	
		
		

	def id(self):
		return self.dataentry['id']
	

	
	def name(self):
		return self.dataentry['Name'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )
	
	def priority(self):
		return self.dataentry['priority']
	
	def city(self):
		return self.dataentry['City'].decode('iso-8859-1').encode('utf8') 

	def country(self):
		return self.dataentry['Country'].decode('iso-8859-1').encode('utf8') 

	def email(self):
		return self.dataentry['e-mail'].decode('iso-8859-1').encode('utf8') 
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8') 
	
	def links(self):
		soup = BeautifulSoup( self.dataentry['link'] )
		return unicode( soup )
	
class OnlineArtDataMapping(SpacetelescopeDataMapping):
	BASE = "/goodies/art/"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/art"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/art/"

	def _create_object(self):
		
		self.obj = OnlineArt( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority = self.priority(),
				artist = OnlineArtAuthor.objects.get(id=self.artist())
				)
		self.obj.save()	

	def artist (self):
		return self.dataentry['artist_id']
	
	def id(self):
		return self.dataentry['id']
	
	def title(self):
		return self.dataentry['Title'].decode('iso-8859-1').encode('utf8') 
			
	def description(self):
		soup = BeautifulSoup( self.dataentry['Description'] )
		return unicode( soup )
	
	def priority(self):
		return self.dataentry['priority']
	
	def city(self):
		return self.dataentry['City'].decode('iso-8859-1').encode('utf8') 

	def country(self):
		return self.dataentry['Country'].decode('iso-8859-1').encode('utf8') 

	def email(self):
		return self.dataentry['e-mail'].decode('iso-8859-1').encode('utf8') 
		
	def credit(self):
		return self.dataentry['credit'].decode('iso-8859-1').encode('utf8') 
	
	def links(self):
		soup = BeautifulSoup( self.dataentry['link'] )
		return unicode( soup )