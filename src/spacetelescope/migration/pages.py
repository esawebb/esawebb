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
from djangoplicity.migration import MigrationError, MigrationTask
from djangoplicity.migration.apps.pages import HTMLPageDocument, nl2space
from dreamweavertemplate import *
from django.utils.html import strip_tags
import tempfile

#
# TODO: Define menu structure for pages
# TODO: Extract links
# TODO: Update all interal links (static files, archives, static pages)


class SpacetelescopePageDocument( HTMLPageDocument ):
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
		# Make sure we also have the entire HTML document in self.soup
		super( SpacetelescopePageDocument, self ).parse()
		
		# Read with dreamweaver
		filepath = self.filepath( self.conf['pages']['root'] )
		
		try:
			self.logger.debug( "Parsing %s..." % filepath )
			self.dwpage = DreamweaverTemplateInstance( filename=filepath )
		except UnicodeDecodeError:
			# Text encoding problems - let BeautifulSoup convert to UTF8			
			#try:
				self.logger.debug( "Problems parsing file - retrying with BeautifulSoup..." )
				
				# Write to temporary file (in UTF8 encoding)
				f = tempfile.NamedTemporaryFile( )
				f.write( unicode( self.soup ).encode( 'utf8' ) )
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
		
	def section(self):
		"""
		Determine the template section of the document.
		"""
		menuitem = self.handle_selected_menu()
		if menuitem:
			try:
				sectionname = self.conf['pages']['section_mapping'][menuitem]
				section = self.conf['pages']['sections'][sectionname]
				return section				
			except KeyError:
				pass
		
		# Default section
		return self.conf['pages']['section']
	
	#
	# Helper method
	#
	def handle_selected_menu(self):
		"""
		Extract the title of the selected main menu item  
		"""
		try:
			div = self.soup.find( attrs = { "class" : "mainMenuArea" } )
			menu = div.find( attrs = { "class" : "mainMenuItemselected" } )
			return strip_tags( "".join( [unicode( x ) for x in menu.contents] ) ).strip()
		except (KeyError, AttributeError):
			return None

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
		val = self.clean_title( val )
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
				
			text = text.strip()
			text = self.convert_entities( strip_tags( text ) )
			
		return text