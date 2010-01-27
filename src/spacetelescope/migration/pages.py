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
from djangoplicity.migration.apps.pages import PageDocument, nl2space
from dreamweavertemplate import *

class SpacetelescopePageDocument( PageDocument ):
	def __init__( self, filename ):
		super( SpacetelescopePageDocument, self ).__init__( filename )
		self._title = None
		self.dwpage = None
	
	def _get_region( self, name ):
		"""
		Get contents of editable region in Dreamweaver page.
		"""
		if name in self.dwpage.page_regions:
			return self.dwpage.page_regions[name]
		else:
			return None
	
	#
	#
	#
	def parse(self, conf):
		self.dwpage = DreamweaverTemplateInstance( filename=self.filepath( conf['pages']['root'] ) )
		self._parsed = True
	
	#
	#
	#
	def title(self):
		""" Title of the document. """
		if not self._title:
			tmp = self.handle_headline() # First try if there's a template title
			tmp = tmp if tmp else self.handle_doctitle()
			self._title = tmp if tmp else self.handle_content_h1() 
		return self._title
	
	def content(self):
		""" Content/body text of document. """
		pagecontent = self._get_region('PageContent')
		contentarea = self._get_region('ContentArea')
		  
		if pagecontent:
			headline = self.handle_headline()
			if not headline:
				return pagecontent
			else:
				return "<h1>%s</h1>\n%s" % (headline,pagecontent)
		elif contentarea:
			return contentarea
		else:
			return None
	
	#
	# Helper method
	#
	def handle_doctitle(self):
		""" Extract doctitle from Dreamweaver template """
		html = self._get_region( "doctitle" )
		val = self.parse_doctitle( html )
		val = self.clean_title( val )
		if val == "":
			return None
		return val
	
	def handle_content_h1(self):
		""" Extract doctitle from Dreamweaver template """
		html = self._get_region( "ContentArea" )
		val = self.parse_first_h1( html )
		val = self.clean_title( val )
		if val == "":
			return None
		return val
	
	def handle_headline(self):
		""" Extract Headline region from Dreamweaver template """
		val = self._get_region( "Headline" )
		return nl2space(val)

	def parse_doctitle( self, html, encoding = None ):
		defaults = {}
		if encoding:
			defaults['fromEncoding'] = encoding
		soup = BeautifulSoup( html, **defaults )
		elem = soup.find( 'title' )
		return "".join( elem.contents ).strip()

	def parse_first_h1( self, html, encoding=None  ):
		defaults = {}
		if encoding:
			defaults['fromEncoding'] = encoding
		soup = BeautifulSoup( html, **defaults )
		elem = soup.find( 'h1' )
		if elem:
			return "".join(elem.contents).strip()
		else:
			return None
		
	def clean_title(self,text):
		"""
		Remove unwanted boiler text from beginning of title.
		"""
		TITLE_PREPENDS = ["The European Homepage For The NASA/ESA Hubble Space Telescope -", "The European Homepage For The NASA/ESA Hubble Space Telescope"]
		for t in TITLE_PREPENDS: 
			if text.startswith( t ):
				text = text.replace( t, "" )
			
		return text.strip()
