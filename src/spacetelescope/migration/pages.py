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
from djangoplicity.migration import MigrationError
from djangoplicity.migration.apps.pages import PageDocument, nl2space
from dreamweavertemplate import *

class SpacetelescopePageDocument( PageDocument ):
	"""
	Migration of a HTML page from spacetelescope.org
	
	The HTML pages are based on Dreamweaver templates and thus
	we can extract the relevant parts pretty easily.
	"""
	
	def __init__( self, filename ):
		super( SpacetelescopePageDocument, self ).__init__( filename )
		self._title = None
		self.encoding = None
		self.dwpage = None
	
	#
	# Parser
	#
	def parse(self, conf):
		"""
		Parse spacetelescope.org HTML page.
		"""
		  
		
		filepath = self.filepath( conf['pages']['root'] )
		try:
			self.logger( conf ).debug( "Parsing %s..." % filepath )
			self.dwpage = DreamweaverTemplateInstance( filename=filepath )
		except UnicodeDecodeError:
			raise MigrationError( "Couldn't decode page with using UTF8", can_continue=True )
		
		# Read contents out to let BeautifulSoup detect the encoding
		#super( SpacetelescopePageDocument, self ).parse( conf )
		#soup = BeautifulSoup( self._file_contents )
		#self.encoding = soup.originalEncoding
		#print self.encoding 
		self._parsed = True
		
	def _get_region( self, name ):
		"""
		Get contents of editable region in Dreamweaver page.
		"""
		if name in self.dwpage.page_regions:
			return self.dwpage.page_regions[name]
		else:
			return None
	
	#
	# Page fields methods - overwrite superclass methods
	#
	def title(self):
		""" 
		Title of the document.
		"""
		if not self._title:
			tmp = self.handle_headline() # First try if there's a template title
			tmp = tmp if tmp else self.handle_doctitle()
			self._title = tmp if tmp else self.handle_content_h1() 
		return self._title
	
	def content(self):
		""" 
		Content/body text of document.
		"""
		pagecontent = self._get_region('PageContent')
		contentarea = self._get_region('ContentArea')
		mainarea = self._get_region('MainArea')
		  
		if pagecontent:
			headline = self.handle_headline()
			if not headline:
				return pagecontent
			else:
				return "<h1>%s</h1>\n%s" % (headline,pagecontent)
		elif contentarea:
			return contentarea
		elif mainarea:
			return mainarea
		else:
			return None
	
	#
	# Helper method
	#
	def handle_doctitle(self):
		""" 
		Extract doctitle from Dreamweaver template 
		"""
		html = self._get_region( "doctitle" )
		val = self.parse_doctitle( html )
		val = self.clean_title( val )
		if val == "":
			return None
		return val
	
	def handle_content_h1(self):
		""" 
		Extract doctitle from Dreamweaver template 
		"""
		html = self._get_region( "ContentArea" )
		val = self.parse_first_h1( html )
		val = self.clean_title( val )
		if val == "":
			return None
		return val
	
	def handle_headline(self):
		""" 
		Extract Headline region from Dreamweaver template 
		"""
		val = self._get_region( "Headline" )
		return nl2space(val)

	def parse_doctitle( self, html ):
		"""
		Extract the contents of the first encountered title-tag. 
		"""
		if html:
			defaults = {}
			if self.encoding:
				defaults['fromEncoding'] = self.encoding
			soup = BeautifulSoup( html, **defaults )
			elem = soup.find( 'title' )
			return "".join( elem.contents ).strip()
		
		return None

	def parse_first_h1( self, html  ):
		"""
		Extract the content of the first encountered h1-tag.
		"""
		if html:
			defaults = {}
			if self.encoding:
				defaults['fromEncoding'] = self.encoding
			soup = BeautifulSoup( html, **defaults )
			elem = soup.find( 'h1' )
			if elem:
				return "".join(elem.contents).strip()
			
		return None
			
		
	def clean_title(self,text):
		"""
		Remove unwanted boiler text from beginning of title.
		"""
		if text:
			TITLE_PREPENDS = ["The European Homepage For The NASA/ESA Hubble Space Telescope -", "The European Homepage For The NASA/ESA Hubble Space Telescope"]
			for t in TITLE_PREPENDS: 
				if text.startswith( t ):
					text = text.replace( t, "" )
				
			return text.strip()
		return text
