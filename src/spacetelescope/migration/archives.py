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
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from datetime import datetime
from django.contrib.redirects.models import Redirect
from djangoplicity.migration import MigrationError
from djangoplicity.migration.apps.archives import CSVDataSource, DataMapping
from djangoplicity.releases.models import Release, ReleaseType, ReleaseImage, ReleaseVideo
from djangoplicity.releases.models import Image, Video
from spacetelescope.archives.models import *
#from spacetelescope.archives.products.models import *
from django.utils.html import strip_tags
from djangoplicity.utils.videothumbnails import format_duration

import csv
import re

numberregex = re.compile( "(\d+(\.\d+)?)")

def calc_priority( p ):
	"""
	Take an integer between 0 and 5 and returns a number
	between 10 and 90
	"""
	return (5-int(p))*16+10


def strip_and_convert( s ):
	"""
	Convert a string with HTML and entities in into
	Unicode string.
	"""
	s = BeautifulSoup( s )
	s = "".join([unicode(x) for x in s.contents])
	s = strip_tags(s)
	s = BeautifulStoneSoup( s,  convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	s = "".join([unicode(x) for x in s.contents])
	return s.strip() 

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
			r,created = Redirect.objects.get_or_create( site = self.conf['pages']['site'], old_path=url )
			if created:
				r.new_path = new_url
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
				if not os.path.exists( new_filepath ):
					os.symlink( old_filepath, new_filepath ) 
			elif copy:
				shutil.copy(old_filepath,new_filepath)
			else:
				pass
				#os.rename( p, new_filepath )
	
	def _dataentry(self,key):
		# attempt lowercase retrieve and then title. otherwise fail
		try:
			return self.dataentry[key]
		except KeyError:
			try:
				return self.dataentry[key.lower()]
			except KeyError:
				return self.dataentry[key.title()]
			
	
	def subject_category( self, type ):
		mapping = self.conf['archives']['%s_category_mapping' % type]
		
		cats = []
		for t in self.topic():
			 try:
			 	c = mapping[t].subject_category
			 	cats.append(c)
			 except KeyError:
			 	print '%s_category_mapping' % type
			 	print "Couldn't get topic %s.." % t
		
		return cats
			
	def heic_release_numbers(self):
		rels = self.release_number()
		return filter( lambda x: x.startswith("heic"), rels )
	
	def nonheic_release_numbers(self):
		rels = self.release_number()
		return filter( lambda x: not x.startswith("heic"), rels )
	
	def topic(self):
		topics = self.get_text_field('topic')
		return map( lambda x: x.strip(), topics.split( "," ) )
	
	def get_text_field( self, fieldname ):
		soup = BeautifulSoup( self._dataentry( fieldname ) )
		return unicode( soup )
	
	def get_boolean( self, fieldname ):
		dat = self._dataentry( fieldname )
		if dat.lower() == "yes":
			return True
		if dat.lower() == "no":
			return False
		return None
	
	def get_number_field( self, fieldname ):
		m = numberregex.search( self._dataentry( fieldname ) )
		if m:
			return m.group(1)
		else:
			return None
	
	def lead(self):
		return strip_and_convert( self.get_text_field('lead') )
	
	def headline(self):
		return strip_and_convert( self.get_text_field('headline') )
	
	def release_date( self ):
		return self._parse_date( self.dataentry['release date/local time Munich (CET or CEST)'] )
	
	def embargo_date( self ):
		return self._parse_date( self.dataentry['Stage date/local time Munich (CET or CEST)'] )
		
	def contacts(self):
		return self.get_text_field('contacts')
	
	def links (self):
		soup = BeautifulSoup( self.dataentry['links'] )
		links = unicode( soup )
		
		p = re.compile("(<br>|<br \/>)") #my @lines = split( /)/, $str);
		
		tmp = p.split( links )
		lines = []
		for i in range( 0, len( tmp ) ):
			if i % 2 == 0:
				lines.append( tmp[i] )
		
		linkp = re.compile("(.+):\s+(http|https|ftp):\/\/(.+)\s*")
		
		output = ""
		for line in lines:
			m = linkp.match( line )
			if m:
				output += '<a href="%s://%s">%s</a><br />' % ( m.group( 2 ), m.group( 3 ), m.group( 1 ) );
			
		return output;
	
	def id(self):
		return self._dataentry('id')
	
	def title(self):
		return strip_and_convert( self._dataentry('Title') ) 
			
	def description(self):
		return self.get_text_field('Description')
	
	def text(self):
		return self.get_text_field('text')
	
	def width(self):
		m = numberregex.search( self._dataentry('Width') )
		if m:
			return m.group(1)
		else:
			return ''
	
	def height(self):
		m = numberregex.search( self._dataentry('Height') )
		if m:
			return m.group(1)
		else:
			return ''
		
	def x_size(self):
		return self._dataentry('X resolution')
	
	def y_size(self):
		return self._dataentry('Y resolution')
	
	def xsize(self):
		return self._dataentry('xsize')
	
	def ysize(self):
		return self._dataentry('ysize')
	
	def resolution(self):
		return self._dataentry('dpi')
	
	def weight(self):
		return self._dataentry('Weight')
		
	def priority(self):
		return calc_priority(self._dataentry('priority'))
		
	def credit(self):
		return self.get_text_field('credit')
		
	def sale(self):
		return self._dataentry('Sale').lower() in ['yes',]
		
	def price(self):
		p = self._dataentry('Price')
		return p if p else 0
	
	def name(self):
		return self.get_text_field( 'Name' ) 

	def city(self):
		return self.get_text_field( 'City' )
	
	def town(self):
		return self.get_text_field( 'Town' )

	def country(self):
		return self.get_text_field( 'Country' )
	
	def email(self):
		return self.get_text_field('e-mail') 
		
	def link(self):
		return self.get_text_field('link')
	
	def duration(self):
		txt = self.get_number_field('duration')
		if txt:
			secs = int(txt)
		
			if secs:
				return format_duration(secs)
		return None 
			
				
				
class ProductDataMapping (SpacetelescopeDataMapping):
	#base data mapping for all products (shop)
	model = None  
	has_pages=False
	has_price=True
	format_mapping = {'thumbs':'thumb'}
	extra_fields = []
	
	def _create_object(self):
		# id, releasetype, title
		
		self.obj = self.model( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				width=self.width(),
				height=self.height(),
				priority=self.priority(),
				credit=self.credit(),
				#delivery=self.delivery(),
			)

		if self.has_price:
			self.obj.price = self.price()
			self.obj.sale = self.sale()
			self.obj.weight = self.weight()

		if self.has_pages:
			self.obj.pages = self.pages()
			
		if self.extra_fields:
			for f in self.extra_fields:
				setattr( self.obj, f, getattr( self, f )() ) 

		self.obj.save()
		
	
	def pages(self):
		if self.has_pages:
			return self._dataentry('Pages')
		else:
			return None
	

	
#
# TOOD: Remove HTML tags from title
# TOOD: Format links
# TODO: connect with images + main image
# TODO: fix release_type
# TODO: import contacts
# TODO: extract contacts???

class NewsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/news"
	format_mapping = {
					'pdf':'pdf',
					'doc':'doc',
					'text':'text',
					'science_paper':'science_papers', 
					}
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/news/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/news/"
	
	# handle layouts
	#TODO handle print layouts
	def _move_resources(self,copy=COPY_INSTEAD_OF_MOVE):
		pass
	
	def _create_object(self):
		# id, releasetype, title
		self.obj = Release( 
				id=self.id(),
				release_type=self.release_type(),
				title=self.title(), 
				headline=self.lead(),
				description=self.text(),
				notes=self.notes(),
				links=self.links_contacts(),
				release_date=self.release_date(),
				embargo_date=self.embargo_date(),
			)
		self.obj.save()
		
#	def id(self):
#		return self.dataentry['id']

	def release_type(self):
		type = self.dataentry['release_type']
		mapping = {'News':'Science Release', 'Photo':'Photo Release'}
		type = mapping[type]
		return ReleaseType.objects.get_or_create( name=type )[0]
	
#	def title(self):
#		return self.dataentry['title']
	
	def links_contacts(self):
		contacts = self.contacts()
		links = self.links()
		
		if contacts:  
			return "%s<div class='contactdata'><h3>Contacts</h3>%s</div>" % ( links, contacts )
		else:
			return links
		
	def notes(self):
		return self.get_text_field('notes')
		

class NewsMainImageDataMapping( SpacetelescopeDataMapping ):
	def _create_object(self):
		# id, releasetype, title
		
		rel = Release.objects.get( id = self.id() )
		
		try:
			im = Image.objects.get( id = self.main_image() )
		
			print rel.id
			print im.id
			ri = ReleaseImage.objects.get( release = rel, archive_item = im )
			ri.main_visual=True
			ri.save()
		except Image.DoesNotExist:
			pass
		except:
			pass
		
	def _create_redirect(self):
		pass
	
	def _move_resources(self):
		pass
	
	def main_image(self):
		return self.get_text_field('main_image')


class VideosDataMapping( SpacetelescopeDataMapping ):
	BASE = "/videos"
	
	format_mapping = {'thumbs':'thumbs'}

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/videos/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/videos/"
	
	def _create_object(self):
		self.obj = Video( 
				id = self.id(),
				# TOPIC 
				priority=self.priority(),
				title=self.title(),
				headline=self.rss_desc(),
				description=self.description(),
				credit=self.credit(),
				file_duration = self.duration(),
				content_server = self.file_url()
			)
		self.obj.save()
		
		heicrels = self.heic_release_numbers()
		if heicrels: 
			for relno in heicrels:
				rel = Release.objects.get( id = relno  )
				ri = ReleaseVideo( release = rel, archive_item = self.obj )
				ri.save()
				
		cats = self.subject_category('videos')
		
		for c in cats:
			self.obj.subject_category.add( c )
			
		self.obj.save()
				
	def release_number(self):
		rels = self.get_text_field('release_number')
		return rels.split( "," )
	
	def file_url(self):
		return self.get_text_field('fileurl')
	
	def rss_desc(self):
		return strip_and_convert( self.dataentry['rss desc'] )
	
	


	

class ImagesDataMapping( SpacetelescopeDataMapping ):
	BASE = "/images"
	
	format_mapping = {'thumbs':'thumbs'}

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/images/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/images/"
	
	def _create_object(self):
		self.obj = Image( 
				id = self.id(),
				priority=self.priority(),
				title=self.title(),
				headline=self.headline(),
				description=self.description(),
				credit=self.credit(),
				old_ids=self.old_ids(),
				# subject name
				# object type
				# facility
				# instrument
				wallpapers = self.wallpaper(),
				zoomify = self.zoomable(),
				width = self.org_width(),
				height = self.org_height(),
				long_caption_link = self.caption_link(),
				press_release_link = self.opo_link(),
				# Simbad
				# subject_category
				type = self.type(),
				spatial_reference_dimension = self.spatial_reference_dimension(),
				spatial_coordinate_frame = self.spatial_coordinate_frame(),
				spatial_equinox = self.spatial_equinox(),
				spatial_reference_value = self.spatial_reference_value(),
				spatial_reference_pixel = self.spatial_reference_pixel(),
				spatial_scale = self.spatial_scale(),
				spatial_rotation = self.spatial_rotation(),
				spatial_coordsystem_projection = self.spatial_coordsystem_projection(),
				spatial_quality = self.spatial_quality(),
				spatial_notes = self.spatial_notes(),
			)
		self.obj.save()
		
		heicrels = self.heic_release_numbers()
		if heicrels: 
			for relno in heicrels:
				rel = Release.objects.get( id = relno  )
				ri = ReleaseImage( release = rel, archive_item = self.obj , order = self.chrono() )
				ri.save()
				
		cats = self.subject_category('images')
		
		for c in cats:
			self.obj.subject_category.add( c )
			
		names = self.subject_names()
		for n in names:
			self.obj.subject_name.add(n)
			
		self.obj.save()
	
	def opo_link(self):
		return self.get_text_field('OPO Press Link')
	
	def caption_link(self):
		return self.get_text_field('OPO Caption link')
	
	def subject_names(self):
		names = self.get_text_field('Subject.Name')
		simbad_compliant = True if self.get_boolean('Simbad') is None or self.get_boolean('Simbad') else False
		
		ret = []
		if names:
			names = map( lambda x: x.strip(), names.split(",") )
			is_first=True
			for n in names:
				if is_first:
					subjectname = self.get_create_subject_name( n, simbad=simbad_compliant )
					is_first = False
				else:
					subjectname = self.get_create_subject_name( n )
				ret.append( subjectname )
				
		return ret

		
	def get_create_subject_name(self, name, simbad=False ):
		name,created = SubjectName.objects.get_or_create( name=strip_and_convert(name) )
		
		if created:
			name.simbad_compliant = simbad
			name.save()
			
		return name
		
	def old_ids(self):
		nonheic = self.nonheic_release_numbers()
		
		if nonheic:
			return "%s (release id)" % (", ".join(nonheic) )
		elif self.alternate_id():
			return "%s (alternative id)" % self.alternate_id()
		else:
			return ""
	
	def alternate_id(self):
		return self.get_text_field("alternative id/OPO id")
	
	def topic(self):
		topics = self.get_text_field("Object Type")
		return map( lambda x: x.strip(), topics.split( "," ) )
	
	def chrono( self ):
		return self.get_number_field('Chrono, subnumber')
	
	def release_number(self):
		rels = self.get_text_field('Release number')
		return rels.split( "," )
	
	def type(self):
		return self.get_text_field('Type')
	
	def wallpaper(self):
		return self.get_boolean('Wallpaper')
	
	def zoomable(self):
		return self.get_boolean('Zoomable')
	
	def org_width(self):
		return self.get_number_field('original pixel width')
	
	def org_height(self):
		return self.get_number_field('original pixel height')
	
	def type(self):
		return self.get_text_field('Type')
	
	def spatial_reference_dimension( self ):
		return self.get_text_field('Spatial.ReferenceDimension')
	
	def spatial_coordinate_frame(self):
		return self.get_text_field('Spatial.CoordinateFrame')
	
	def spatial_equinox(self):
		return self.get_text_field('Spatial.Equinox')

	def spatial_reference_value(self):
		return self.get_text_field('Spatial.ReferenceValue')
	
	def spatial_reference_pixel(self):
		return self.get_text_field('Spatial.ReferencePixel')
	
	def spatial_scale(self):
		return self.get_text_field('Spatial.Scale')
	
	def spatial_rotation(self):
		return self.get_text_field('Spatial.Rotation')
	
	def spatial_coordsystem_projection(self):
		return self.get_text_field('Spatial.CoordsystemProjection')
	
	def spatial_quality(self):
		return self.get_text_field('Spatial.Quality')
	
	def spatial_notes(self):
		return self.get_text_field('Spatial.Notes')
	

class EducationalMaterialsDataMapping( ProductDataMapping ):
	model = EducationalMaterial
	BASE = "/kidsandteachers/education"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'highres_pdf':'pdf',
					  'lowres_pdf':'pdfsm',
					  }

	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/kidsandteachers/education/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/education/"
		

class KidsDrawingsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/kidsandteachers/drawings"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/kidsandteachers/drawings/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/drawings/"
	
	def _create_object(self):
		# id, releasetype, title
		self.obj = KidsDrawing( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				name = self.name(),
				age = self.age(),
				city = self.town(),
				country = self.country(),
			)
		
	def age(self):
		return self.get_number_field( 'Age' )


#TODO copy pdf resources ALL to each month/year
class CalendarsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/goodies/calendar"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'medium':'medium',
					  'large':'large',
					  'pdf_a3':'pdf',
					  'pdf_a4':'pdfsm',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/calendar/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/calendars/"
	
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


	
	def _create_object(self):
		# id, releasetype, title
		self.obj = Calendar( 
				id=self.id(),
				title=self.title(),
				year=self.year(),
				month=self.month(),
				description=self.caption(),
				#priority=self.priority(),
				credit=self.credit(),
			)
		self.obj.save()
		
	
	def id(self):
		return "cal%s%s" % (self.year(),self.MONTHS[self.dataentry['month']]  )
			
	def year (self):
		return int(self.dataentry['year'])
	
	def month (self):
		return int(self.MONTHS[self.dataentry['month']])
	
	
	def caption(self):
		soup = BeautifulSoup( self.dataentry['caption'] )
		return unicode( soup )
		
	def priority(self):
		return 0 # there is no prio in csv

		
class SlideShowDataMapping( SpacetelescopeDataMapping ):
	BASE = "/goodies/slideshows"
	
	format_mapping = {'thumbs':'thumb',
					  #'flash':'flash',
					  #TODO: handle flash

					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/slideshows/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/slideshows/"
	
	def _create_object(self):
		# id, releasetype, title
		self.obj = SlideShow( 
				id=self.id(),
				title = self.title(),
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				x_size = self.xsize(),
				y_size = self.ysize(),
			)
		self.obj.save()


class CDROMDataMapping(ProductDataMapping):
	model = CDROM
	BASE = "/goodies/cdroms"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'medium':'medium',
					  'large':'large',
					  'zip':'zip',
					  }
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/cdroms/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/cdroms/"
	
class BookDataMapping(ProductDataMapping):
	model = Book
	BASE = "/about/further_information/books"
	format_mapping = {'thumbs':'thumb',
				  'original':'original',
				  'medium':'medium',
				  'large':'large',
				  'screen':'screen',
				  'pdf':'pdf',
				  }
	
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/books/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/books/"
	
class BrochureDataMapping(ProductDataMapping):
	model = Brochure
	BASE = "/about/further_information/brochures"
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
	NEW_FMT_ROOT = "/hubbleroot/static/archives/brochures/"
	
class MerchandiseDataMapping(ProductDataMapping):
	model = Merchandise
	BASE = "/goodies/merchandise"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/merchandise/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/merchandise/"
	
class NewsletterDataMapping( ProductDataMapping ):
	model = Newsletter
	BASE = "/about/further_information/newsletters"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf',
					  }
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/newsletters/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/newsletters/"

class PostCardDataMapping(ProductDataMapping):
	model = PostCard
	BASE = "/goodies/postcards"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/postcards/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/postcards/"

class PosterDataMapping(ProductDataMapping):
	model = Poster
	BASE = "/goodies/posters"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/posters/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/posters/"
	
	extra_fields = ['x_size','y_size','resolution']


class StickerDataMapping(ProductDataMapping):
	model = Sticker
	BASE = "/extras/stickers"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/stickers/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/stickers/"


class PressKitDataMapping(ProductDataMapping):
	model = PressKit
	has_price = False
	BASE = "/about/further_information/presskits"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf'
					  }
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/presskits/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/presskits/"
	
	
	

# ORG
#TODO copy image resources
class AnnouncementDataMapping( ProductDataMapping ):

	BASE = "/updates"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'newsmini':'newsmini',
					  }
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/updates/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/announcements/"
	
	def _create_object(self):
		self.obj = Announcement( 
				id=self.id(),
				title = self.title(),
				release_date = self.release_date(),
				embargo_date = self.embargo_date(),
				description=self.text(),
				contacts=self.contacts(),
				links = self.links(),
			)
		self.obj.save()
		
	def old_urls(self):
		"""
		Return a list of old URLs where this archive item was accessible.
		"""
		return ["%s/html/%s.html" % (self.BASE, super(AnnouncementDataMapping,self).id() ),]
		
	def id(self):
		id = super(AnnouncementDataMapping,self).id()
		id = id.replace('update','ann')
		return id
	
	def _find_old_resource(self, fmt ):
		old_path = os.path.join( self.OLD_FMT_ROOT, fmt )
		#look for files named with self.obj.id in old_path 
		
		p = old_path
		for ext in self.VALID_EXTS:
			old_path = os.path.join(p, super(AnnouncementDataMapping,self).id() + ext)
			if os.path.exists(old_path):
				return old_path

	
class ConferencePosterDataMapping(SpacetelescopeDataMapping):
	BASE = "/about_us/conference_posters"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }
	
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about_us/conference_posters/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/conference_posters/"

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
				x_size = self.x_size(),
				y_size = self.y_size(),
				)
		self.obj.save()	
		
	
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
	NEW_FMT_ROOT = "/hubbleroot/static/archives/logos/"

	def _create_object(self):
		
		self.obj = Logo( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				)
		self.obj.save()	


class TechnicalDocumentDataMapping(ProductDataMapping):
	model = TechnicalDocument
	BASE = "/about/further_information/techdocs"
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'pdf':'pdf',
					  }
	has_pages=True
	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/about/further_information/techdocs/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/techdocs/"
	


class ExhibitionDataMapping(SpacetelescopeDataMapping):
	BASE = "/projects/exhibitions"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/projects/exhibitions/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/exhibitions/"

	def _create_object(self):
		
		self.obj = Exhibition( 
				id=self.id(),
				title=self.title(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				)
		self.obj.save()	
		
	
class FITSImageDataMapping(SpacetelescopeDataMapping):
	BASE = "/projects/fits_liberator/fitsimages"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/projects/fits_liberator/fitsimages/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/fitsimages/"

	def _create_object(self):
		
		self.obj = FITSImage( 
				id=self.id(),
				title=self.title(),
				name=self.name(), 
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				city = self.city(),
				country = self.country(),
				)
		self.obj.save()	
		
		
class UserVideoDataMapping(SpacetelescopeDataMapping):
	BASE = "/videos/users_videos"
	
	format_mapping = {'thumbs':'thumb',
					  'broadcast':'broadcast',
					  'h264':'h264',
					  'large':'large',
					  '180px' : '180px',
					  '320px' : '320px',
					  'broadcast' : 'broadcast',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/videos/user_videos/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/uservideos/"

	def _create_object(self):
		
		self.obj = UserVideo( 
				id=self.id(),
				title=self.title(),
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				city = self.city(),
				country = self.country(),
				email = self.email(),
				link = self.link(),
				duration = self.duration(),
				)
		self.obj.save()	

			

class OnlineArtAuthorDataMapping(SpacetelescopeDataMapping):
	BASE = "/goodies/art"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }



	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/art/"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/artists/"

	def _create_object(self):
		
		self.obj = OnlineArtAuthor( 
				id=self.id(),
				name=self.name(), 
				description=self.description(),
				city = self.city(),
				country = self.country(),
				email = self.email(),
				link = self.link(),
				priority = self.priority()
				)
		self.obj.save()	

	
class OnlineArtDataMapping(SpacetelescopeDataMapping):
	#BASE = "/goodies/art"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/art"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/art/"

	def _create_object( self ):
		
		self.obj = OnlineArt( 
				id = self.id(),
				title = self.title(),
				description = self.description(),
				priority = self.priority(),
				artist = OnlineArtAuthor.objects.get( id = self.artist() )
								)
		self.obj.save()	


	def artist (self):
		return self.get_text_field('artist_id')
	

class PresentationDataMapping(SpacetelescopeDataMapping):
	BASE = "/goodies/presentations"
	
	format_mapping = {'thumbs':'thumb',
					  'original':'original',
					  'screen':'screen',
					  'medium':'medium',
					  'large':'large',
					  'ppt':'ppt',
					  'pps':'pps',
					  'pdf':'pdf',
					  }

	OLD_FMT_ROOT = "/Volumes/webdocs/spacetelescope/docs/goodies/presentations"
	NEW_FMT_ROOT = "/hubbleroot/static/archives/presentations/"

	def _create_object(self):
		
		self.obj = Presentation( 
				id=self.id(),
				title=self.title(),
				description=self.description(),
				priority=self.priority(),
				credit=self.credit(),
				)
		self.obj.save()	