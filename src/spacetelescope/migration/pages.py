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
import tempfile

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
	def parse(self):
		"""
		Parse spacetelescope.org HTML page.
		"""
		filepath = self.filepath( self.conf['pages']['root'] )
		
		try:
			self.logger.debug( "Parsing %s..." % filepath )
			self.dwpage = DreamweaverTemplateInstance( filename=filepath )
		except UnicodeDecodeError:
			# Text encoding problems - let BeautifulSoup convert to UTF8			
			#try:
				self.logger.debug( "Problems parsing file - retrying with BeautifulSoup..." )
				# Read and parse file with BeautifulSoup
				super( SpacetelescopePageDocument, self ).parse()
				soup = BeautifulSoup( self._file_contents )

				# Write to temporary file (in UTF8 encoding)
				f = tempfile.NamedTemporaryFile( )
				f.write( unicode(soup).encode('utf8') )
				f.flush()
				
				# Read temporary file (which is now converted to UTF8 )
				self.dwpage = DreamweaverTemplateInstance( filename=f.name )
				
				# Close and automatically delete temporary file.
				f.close()
			#except:
			#	raise MigrationError( "Couldn't decode HTML page.", can_continue=True )
		
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
			
			if not self._title:
				self._title = "NO TITLE"
			 
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
			return ""
	
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
