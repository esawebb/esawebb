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
from spacetelescope.archives.org.models import *

import csv

COPY_INSTEAD_OF_MOVE = True

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
	
	def _find_old_resource(self, fmt ):
		old_path = os.path.join( self.OLD_FMT_ROOT, fmt )
		old_path = os.path.join(old_path, self.obj.id + '.jpg')
		#look for files named with self.obj.id in old_path 
		
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
			self.logger.debug( "%s resource from %s to %s..." % (action,old_filepath,new_filepath) )
			if copy:
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
		
		

# TODO
class EducationalMaterialsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/kidsandteachers/educational"
	
	format_mapping = {'thumbs':'thumb'}

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
	
	format_mapping = {'thumbs':'thumb'}

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

class KidsDrawingsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/kidsandteachers/drawings"
	
	format_mapping = {'thumbs':'thumb'}

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



class CalendarsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/goodies/calendars"
	
	format_mapping = {'thumbs':'thumb'}

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
		id = "%s%02d.jpg" % (unicode(self.obj.year)[2:],self.obj.month)
		old_path = os.path.join(old_path, id)
		print old_path
		#look for files named with self.obj.id in old_path 
		
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
	
	format_mapping = {'thumbs':'thumb'}

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
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/cdroms/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/cdroms/"
	
class BookDataMapping(ProductDataMapping):
	model = Book
	BASE = "/products/books"
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/books/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/books/"
	
class BrochureDataMapping(ProductDataMapping):
	model = Brochure
	BASE = "/products/brochures"
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/brochures/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/brochures/"
	
class MerchandiseDataMapping(ProductDataMapping):
	model = Merchandise
	BASE = "/products/merchandise"

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/merchandise/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/merchandise/"
	
class NewsletterDataMapping(ProductDataMapping):
	model = Newsletter
	BASE = "/products/newsletters"
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/newsletters/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/newsletters/"

class PostCardDataMapping(ProductDataMapping):
	model = PostCard
	BASE = "/products/postcards"

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/postcards/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/postcards/"

class PosterDataMapping(ProductDataMapping):
	model = Poster
	BASE = "/products/posters"

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/posters/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/posters/"

class StickerDataMapping(ProductDataMapping):
	model = Sticker
	BASE = "/products/stickers"

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/stickers/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/stickers/"


class PressKitDataMapping(ProductDataMapping):
	model = PressKit
	BASE = "/products/presskits"
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/presskits/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/presskits/"
	
	
	
class TechnicalDocumentDataMapping(ProductDataMapping):
	model = TechnicalDocument
	BASE = "/about_us/techdocs"
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/techdocs/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/techdocs/"
	

# ORG

class AnnouncementDataMapping (ProductDataMapping):
	BASE = "/updates"
	
	format_mapping = {'thumbs':'thumb'}

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/updates/"
	NEW_FMT_ROOT = "/Users/luis/Workspaces/pttu/spacetelescope.org/static/announcements/"
	
	
	
	def _create_redirect(self):
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
			r.save()

	
	def _create_object(self):
		self.obj = Announcement( 
				id=self.id(),
				title = self.title(),
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				x_size = self.x_size(),
				y_size = self.y_size(),
			)
		self.obj.save()
		
		self.contact_obj = AnnouncementContact()
		
		self.contact_obj.save()
		
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