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
from djangoplicity.announcements.models import Announcement, AnnouncementImage
from djangoplicity.migration import MigrationError, MigrationTask
from djangoplicity.migration.apps.archives import CSVDataSource, DataMapping
from djangoplicity.releases.models import Release, ReleaseType, ReleaseImage, ReleaseVideo
from djangoplicity.releases.models import Image, Video
from djangoplicity.products.models import *
from djangoplicity.media.models import ImageExposure
import djangoplicity.metadata.models as metadata
from djangoplicity.metadata.consts import *
#from spacetelescope.archives.products.models import *
from django.utils.html import strip_tags
from djangoplicity.utils.videothumbnails import format_duration

import csv
import re
import glob
import sys    # for exception handling

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

COPY_INSTEAD_OF_MOVE = False
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
	


class ImagesAVMDataMapping( ImagesDataMapping ):
	def run(self):
		# Find image.
		# Determine if something has to be done
		id = self.id()
		
		try:
			im = Image.objects.get( id=id )
		except Exception, e:
			self.logger.error("Could not find image %(id)s - check https://www.spacetelescope.org/admin/history/?s=%(id)s" % { 'id' : id } )
			return
			#raise MigrationError( unicode(e) )
			
		#print '\n'#, im.id
		#self.exposures(im,id)    # checks if the number of exposures in the CSV match with the number of ImageExposure objects
		self.coordinate(im,id)
		
	def coordinate(self, im, id):
		# ANALYSE cordinate metadata
		# ========================================================================
		# Coordinate Metadata 
		# ========================================================================
#		spatial_coordinate_frame = metadatafields.AVMSpatialCoordinateFrameField() CoordinateFrame
#		spatial_equinox = metadatafields.AVMSpatialEquinoxField() Equinox
#		spatial_reference_value = metadatafields.AVMSpatialReferenceValueField() ReferenceValue
#		spatial_reference_dimension = metadatafields.AVMSpatialReferenceDimensionField() ReferenceDimension
#		spatial_reference_pixel = metadatafields.AVMSpatialReferencePixelField()  ReferencePixel
#		spatial_scale = metadatafields.AVMSpatialScaleField() Scale
#		spatial_rotation = metadatafields.AVMSpatialRotationField() Rotation
#		spatial_coordsystem_projection = metadatafields.AVMSpatialCoordsystemProjectionField() CoordsystemProjection
#		spatial_quality = metadatafields.AVMSpatialQualityField()
#		spatial_notes =  metadatafields.AVMSpatialNotesField()
#		spatial_fits_header =  metadatafields.AVMSpatialNotesField()

#		spatial_coordinate_frame 
		if self._dataentry('Spatial.CoordinateFrame'):
			csv = self._dataentry('Spatial.CoordinateFrame').strip().replace(' ','')	
			db  = im.spatial_coordinate_frame.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,': ',db, ' <> CSV: ',  csv

#		spatial_equinox 
		if self._dataentry('Spatial.Equinox'):
			csv = self._dataentry('Spatial.Equinox').strip().replace(' ','')	
			db  = im.spatial_equinox.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_equinox: ',db, ' <> CSV: ',  csv
#		spatial_reference_value 
		if self._dataentry('Spatial.ReferenceValue'):
			csv = self._dataentry('Spatial.ReferenceValue').strip().replace(' ','')	
			db  = im.spatial_reference_value.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_reference_value: ',db, ' <> CSV: ',  csv
#		spatial_reference_dimension 
		if self._dataentry('Spatial.ReferenceDimension'):
			csv = self._dataentry('Spatial.ReferenceDimension').strip().replace(' ','')	
			db  = im.spatial_reference_dimension.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_reference_dimension: ',db, ' <> CSV: ',  csv
#		spatial_reference_pixel 
		if self._dataentry('Spatial.ReferencePixel'):
			csv = self._dataentry('Spatial.ReferencePixel').strip().replace(' ','')	
			db  = im.spatial_reference_pixel.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_reference_pixel: ',db, ' <> CSV: ',  csv
#		spatial_scale 
		if self._dataentry('Spatial.Scale'):
			csv = self._dataentry('Spatial.Scale').strip().replace(' ','')	
			db  = im.spatial_scale.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_scale: ',db, ' <> CSV: ',  csv
#		spatial_rotation 
		if self._dataentry('Spatial.Rotation'):
			csv = self._dataentry('Spatial.Rotation').strip().replace(' ','')	
			db  = im.spatial_rotation.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_rotation: ',db, ' <> CSV: ',  csv
			
#		spatial_coordsystem_projection 
		if self._dataentry('Spatial.CoordsystemProjection'):
			csv = self._dataentry('Spatial.CoordsystemProjection').strip().replace(' ','')	
			db  = im.spatial_coordsystem_projection.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_coordsystem_projection: ',db, ' <> CSV: ',  csv

#		spatial_quality 
		if self._dataentry('Spatial.Quality'):
			csv = self._dataentry('Spatial.Quality').strip().replace(' ','')	
			db  = im.spatial_quality.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_quality: ',db, ' <> CSV: ',  csv
#		spatial_notes 
		if self._dataentry('Spatial.Notes'):
			csv = self._dataentry('Spatial.Notes').strip().replace(' ','')	
			db  = im.spatial_notes.replace(' ','')
			if self.CSVDB(csv,db): pass
			else: print id,' spatial_notes: ',db, ' <> CSV: ',  csv

#		spatial_fits_header CSV?

	def CSVDB(self,a,b):
		ret = False
		a = a.strip().replace(' ','')
		b = b.strip().replace(' ','')
		if a == b: ret = True
		else:
			a = a.split(';')
			b = b.split(';')
			if len(a) == len(b): 
				for i in range(0,len(a),1):
					ret = True
					#print i,a[i],b[i]
					if a[i].find('.') > -1:
						rp = a[i]
						fp = rp.find('.')
						a[i] = rp[:fp] + '.' + rp[fp:].replace('.','')
							#a, in the CSV it is sometimes like 123.456.789
							#b, in the DB it is like 123.123456
					try:
						if abs(float(a[i]) - float(b[i])) > 0.00001: ret = False
					except: ret = False	
			else: ret = False
		return ret 

	def exposures(self, im, id):
		# analyses the image exposure related fields in the csv-file
		# determins the number of exposures from the csv and compares
		# it to the number of exposures in the image objects
		
		# Analyse CSV-file and fill lists
		DatasetID = ['']
		IntegrationTimes = [''] 
		StartTimes = [''] 
		CentralWavelengths = [''] 
		Bandpasses = [''] 
		Bands = [''] 
		ColorAssignments = [''] 
		Instruments = ['']
		Facilities = ['']
		
		if self._dataentry('Facility'):
			Facilities = [self._dataentry('Facility').strip()]
			# print im.id, Facilities
			
		if self._dataentry('Instrument'):
			Instruments = self._dataentry('Instrument')
			if Instruments.find(',') > -1:
				Instruments = [Instrument.strip() for Instrument in self._dataentry('Instrument').split(',')]
			elif Instruments.find('and') > -1:
				Instruments = [Instrument.strip() for Instrument in self._dataentry('Instrument').split('and')]
			elif Instruments.find('&') > -1:
				Instruments = [Instrument.strip() for Instrument in self._dataentry('Instrument').split('&')]
			elif Instruments.find(';') > -1:
				Instruments = [Instrument.strip() for Instrument in self._dataentry('Instrument').split(';')]
			else: Instruments = [self._dataentry('Instrument').strip()]
			# print im.id, Instruments
			
		# "spectral_color_assignment = metadatafields.AVMSpectralColorAssignmentField() <> _dataentry('Spectral.ColorAssignment')"
		if self._dataentry('Spectral.ColorAssignment'):
			ColorAssignments = [ColorAssignment.strip() for ColorAssignment in self._dataentry('Spectral.ColorAssignment').split(';')]
			# print im.id, ColorAssignments		
		
		# "spectral_band = metadatafields.AVMSpectralBandField() <> _dataentry('Spectral.Band')"
		if self._dataentry('Spectral.Band'):
			Bands = [Band.strip() for Band in self._dataentry('Spectral.Band').split(';')]
			# remove all entries that are not in SPECTRAL_BAND_CHOICES
			for i in range(0,len(Bands),1):
				if (Bands[i], Bands[i]) not in SPECTRAL_BAND_CHOICES:
					print i, Bands[i], "not in SPECTRAL_BAND_CHOICES"
					Bands.pop(i)
 			# print im.id,  Bands
			
		# "spectral_bandpass = metadatafields.AVMSpectralBandpassField() <> Spectral.Bandpass"
		if self._dataentry('Spectral.Bandpass'):
			Bandpasses = [Bandpass.strip() for Bandpass in self._dataentry('Spectral.Bandpass').split(';')]
			# print im.id, Bandpasses		
		
		# "spectral_central_wavelength = metadatafields.AVMSpectralCentralWavelengthField() <> _dataentry('Spectral.CentralWavelength')"
		if self._dataentry('Spectral.CentralWavelength'):
			CentralWavelengths = [CentralWavelength.strip() for CentralWavelength in self._dataentry('Spectral.CentralWavelength').split(';')]
			# print im.id, CentralWavelengths
		
		# "temporal_start_time = metadatafields.AVMTemporalStartTimeField() <> _dataentry('Temporal.StartTime')"
		if self._dataentry('Temporal.StartTime'):
			StartTimes = [StartTime.strip() for StartTime in self._dataentry('Spectral.StartTime').split(';')]
			# print im.id, StartTimes
						
		# "temporal_integration_time = metadatafields.AVMTemporalIntegrationTimeField() <> _dataentry('Temporal.IntegrationTime')"
		if self._dataentry('Temporal.IntegrationTime'):
			IntegrationTimes = [IntegrationTime.strip() for IntegrationTime in self._dataentry('Spectral.IntegrationTime').split(';')]
			# print im.id, IntegrationTimes
						
		# "dataset_id = metadatafields.AVMDatasetIDField() <> _dataentry('DatasetID')"
		if self._dataentry('DatasetID'):
			DatasetID = [self._dataentry('DatasetID').strip()]
			# print im.id, DatasetID


		n_exposures = max(len(DatasetID),
						len(IntegrationTimes), 
						len(StartTimes), 
						len(CentralWavelengths), 
						len(Bandpasses), 
						len(Bands), 
						len(ColorAssignments), 
						len(Instruments),
						len(Facilities))
		sum = len(DatasetID[0])+len(IntegrationTimes[0])+len(StartTimes[0])+len(CentralWavelengths[0])+len(Bandpasses[0])+len(Bands[0])+len(ColorAssignments[0]) #+len(Instruments)+len(Facilities)
		print 'NE:', im.id, sum
		if sum > 0: 
			print "DDD", im.id, (DatasetID),(IntegrationTimes), (StartTimes),(CentralWavelengths),(Bandpasses), (Bands), (ColorAssignments)
		print (len(DatasetID),
						len(IntegrationTimes), 
						len(StartTimes), 
						len(CentralWavelengths), 
						len(Bandpasses), 
						len(Bands), 
						len(ColorAssignments), 
						len(Instruments),
						len(Facilities))
		#print n_exposures
		
		#print "Check, how many ImageExposures exist for id", im.id
		
		IEs = ImageExposure.objects.filter( image = im.id)
		diag = ''
		if len(IEs) == 0: diag = 'create all Exposures'
		if len(IEs) == n_exposures: diag = 'fill existing Exposures'
		if len(IEs) > n_exposures: diag = "that's strange"
		
		print im.id,'Exposures in DB:', len(IEs),'    Exposures in csv:', n_exposures, '  ', diag
		return
	
		print len(IEs)
		print "singleIE.image, singleIE.instrument, singleIE.facility, singleIE.spectral_band"
		for singleIE in IEs:
			print singleIE.image, singleIE.instrument, singleIE.facility, singleIE.spectral_band
		
		
		for exp in range(0 ,n_exposures, 1):
			print "Exp", exp
			IE = ImageExposure(image = im)
		 	facility = metadatafields.AVMFacilityField()
		#	instrument = metadatafields.AVMInstrumentField()
		#	spectral_color_assignment = metadatafields.AVMSpectralColorAssignmentField()
		#	spectral_band = metadatafields.AVMSpectralBandField()
		#	spectral_bandpass = metadatafields.AVMSpectralBandpassField()
		#	spectral_central_wavelength = metadatafields.AVMSpectralCentralWavelengthField()
		#	temporal_start_time = metadatafields.AVMTemporalStartTimeField()
		#	temporal_integration_time = metadatafields.AVMTemporalIntegrationTimeField()
		#	dataset_id = metadatafields.AVMDatasetIDField()
			# Facilities
#			if len(Facilities) <= 1:		
#				IE.facility = metadatafields.AVMFacilityField(Facilities[0])	
#				#IE.facility = metadata.Facility(Facilities[0])
#				metadata.Facility(Facilities[0])
#			elif len(Facilities) == n_exposures:
#				IE.facility = metadata.Facility(Facilities[exp])
#			else:
#				print "len(Facilities): %d, n_exp: %d\n" % (len(Facilities),  n_exposures)
##			# Instruments
#			if len(Instruments) <= 1:			
#				IE.instrument = metadata.Instrument(Instruments[0])
#			elif len(Instruments) == n_exposures:
#				IE.instrument = metadata.Instrument(Instruments[exp])
#			else:
#				print "len(Instruments): %d, n_exp: %d\n" % (len(Instruments),  n_exposures)
#			# ColorAssignments
#			if len(ColorAssignments) <= 1:			
#				IE.spectral_color_assignment = ColorAssignments[0]
#			elif len(ColorAssignments) == n_exposures:
#				IE.spectral_color_assignment = ColorAssignments[exp]
#			else:
#				print "len(ColorAssignments): %d, n_exp: %d\n" % (len(ColorAssignments),  n_exposures)
			# Bands
			if len(Bands) <= 1:			
				IE.spectral_band = Bands[0]
			elif len(Bands) == n_exposures:
				IE.spectral_band = Bands[exp]
			else:
				print "len(Bands): %d, n_exp: %d\n" % (len(Bands),  n_exposures)
#			# Bandpasses
#			if len(Bandpasses) <= 1:			
#				IE.spectral_bandpass = Bandpasses[0]
#			elif len(Bandpasses) == n_exposures:
#				IE.spectral_bandpass = Bandpasses[exp]
#			else:
#				print "len(Bandpasses): %d, n_exp: %d\n" % (len(Bandpasses),  n_exposures)
#			# CentralWavelengths
#			if len(CentralWavelengths) <= 1:			
#				IE.spectral_central_wavelength = CentralWavelengths[0]
#			elif len(CentralWavelengths) == n_exposures:
#				IE.spectral_central_wavelength = CentralWavelengths[exp]
#			else:
#				print "len(CentralWavelengths): %d, n_exp: %d\n" % (len(CentralWavelengths),  n_exposures)
#			# StartTimes
#			if len(StartTimes) <= 1:			
#				IE.temporal_start_time = StartTimes[0]
#			elif len(StartTimes) == n_exposures:
#				IE.temporal_start_time = StartTimes[exp]
#			else:
#				print "len(StartTimes): %d, n_exp: %d\n" % (len(StartTimes),  n_exposures)
#			# IntegrationTimes
#			if len(IntegrationTimes) <= 1:			
#				IE.temporal_integration_time = IntegrationTimes[0]
#			elif len(IntegrationTimes) == n_exposures:
#				IE.temporal_integration_time = IntegrationTimes[exp]
#			else:
#				print "len(IntegrationTimes): %d, n_exp: %d\n" % (len(IntegrationTimes),  n_exposures)
#			# DatasetID
#			if len(DatasetID) <= 1:			
#				IE.dataset_id = DatasetID[0]
#			elif len(DatasetID) == n_exposures:
#				IE.dataset_id = DatasetID[exp]
#			else:
#				print "len(DatasetID): %d, n_exp: %d\n" % (len(DatasetID),  n_exposures)
#	
			print IE.facility, IE.instrument, IE.spectral_color_assignment, IE.spectral_band, IE.spectral_bandpass, IE.spectral_central_wavelength, IE.temporal_start_time, IE.temporal_integration_time, IE.dataset_id
			print "Try to save object IE"
			try:
				pass 
				#IE.save()
			except:
				print "IE.save() failed"
				print "Unexpected error:", sys.exc_info()[0]
    			

#		ImageExposure( image=im, spectral_band=..)
#		print self._dataentry('Subject.Category')
#		print self._dataentry('ReferenceURL')
#		print self._dataentry('Date')
#		print self._dataentry('Type')
#		print self._dataentry('Image.ProductQuality')
#		print self._dataentry('Spectral.ColorAssignment')x
#		print self._dataentry('Spectral.Band')x
#		print self._dataentry('Spectral.Bandpass')x
#		print self._dataentry('Spectral.CentralWavelength')x
#		print self._dataentry('Spectral.Notes')
#		print self._dataentry('Temporal.StartTime')x
#		print self._dataentry('Temporal.IntegrationTime')x
#		print self._dataentry('DatasetID')x
#		print self._dataentry('Spatial.ReferenceDimension')
#		print self._dataentry('Spatial.CoordinateFrame')
#		print self._dataentry('Spatial.Equinox')
#		print self._dataentry('Spatial.ReferenceValue')
#		print self._dataentry('Spatial.ReferencePixel')
#		print self._dataentry('Spatial.Scale')
#		print self.spatial_rotation()
#		print self._dataentry('Spatial.Rotation')
#		print self._dataentry('Spatial.CoordsystemProjection')
#		print self._dataentry('Spatial.CDMatrix')
#		print self._dataentry('Spatial.Quality')
#		print self._dataentry('Spatial.Notes')
#		print self._dataentry('Publisher')
#		print self._dataentry('PublisherID')
#		print self._dataentry('ResourceID')
#		print self._dataentry('ResourceURL')
#		print self._dataentry('MetadataVersion')
#		print self._dataentry('MetadataDate')
#		print self._dataentry('RelatedResources')
#		print self._dataentry('ObjectDistance')
#		print self._dataentry('DistortionCorrection')
	


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
		self.obj.save()
		
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
		
		
class AnnouncementResourcesToImagesTask (MigrationTask):
	
	OLD_ROOT = "/Volumes/webdocs/hubble/docs/static/archives/announcements"
	FORMATS_TO_MOVE = [('original','original'),('newsmini','newsmini'),('screen','screen'),('thumb','thumbs'),('large','large'),('medium','medium')]
	NEW_ROOT = "/Volumes/webdocs/hubble/docs/static/archives/images"
	
	
	#finished on 0712
	
	def run(self):
		# reset
		#for annimg in AnnouncementImage.objects.all():
		#	print "deleting %s" % annimg
		#	annimg.archive_item.delete()

		# go
		announcements = Announcement.objects.all()
		
		for announcement in announcements:
			img = self._create_object(announcement)
			self._add_image(announcement,img)
			print "added %s" % img.id
			#self._move_resources(announcement, img)

			
	def _create_object(self,ann):
		try:
			image = Image.objects.get(id=ann.id)
			#print "image with id %s already exists" % ann.id
			#print image.id
			return image
		    
		except Image.DoesNotExist:
			pass
			
		image = Image( 
				id = ann.id,
				title=ann.title,
				description=ann.description,
				priority = 0,
			)
		image.save()
		return image
	
	def _add_image(self,ann,img):
		try:
			AnnouncementImage.objects.get(announcement=ann,archive_item=img)
		except AnnouncementImage.DoesNotExist:
			animg = AnnouncementImage(announcement=ann,
								  main_visual = True,
								  archive_item = img)
			animg.save()
		return
	
	def _move_resources(self,ann,img):
		for format,new_format in self.FORMATS_TO_MOVE:
			old_path = os.path.join (self.OLD_ROOT,format)
			new_path = os.path.join (self.NEW_ROOT,new_format)
			for f in glob.glob (os.path.join (old_path, '%s.*'% ann.id)):
				dir,filename = os.path.split(f)
				p = os.path.join(new_path,filename)
				print "Copying %s to %s" % (f,p )
				if os.path.isfile(p):
					print "%s already exists, skipping" % p
				else:
					shutil.copy(f,p)
		return ann	