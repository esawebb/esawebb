# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from BeautifulSoup import BeautifulSoup
from datetime import datetime
from django.contrib.redirects.models import Redirect
from djangoplicity.migration import MigrationError
from djangoplicity.migration.apps.archives import CSVDataSource, DataMapping
from djangoplicity.releases.models import Release, ReleaseType
from djangoplicity.releases.models import Image
import csv


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
		Return a list of old URLs where this resource was accessible.
		"""
		return ["%s/html/%s.html" % (self.BASE, self.obj.id),]
	
	def _create_redirect(self):
		"""
		Setup redirects for the archive item.
		"""
		new_url = self.obj.get_absolute_url()
		for url in self.old_urls():
			r = Redirect( site = self.conf['pages']['site'], old_path=url, new_path=new_url )
			r.save()

#
# TOOD: Remove HTML tags from title
# TOOD: Format links
# TODO: connect with images + main image
# TODO: fix release_type
# TODO: import contacts
# TODO: extract contacts???

class NewsDataMapping( SpacetelescopeDataMapping ):
	BASE = "/news"
	
	def run(self):
		self._create_object()
		self._create_redirect()
		
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
		