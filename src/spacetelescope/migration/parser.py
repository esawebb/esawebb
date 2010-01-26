# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

from dreamweavertemplate import *
from BeautifulSoup import BeautifulSoup

class DocumentParser( object ):
	"""
	Basic document parser which just reads everything in the file
	"""
	@staticmethod
	def parse( filename ):
		f = open( filename )
		contents = f.read()
		f.close()
		return contents

class DreamweaverPageParser( DocumentParser ):
	"""
	Class for parsing an HTML page connect to a Dreamweaver page.
	"""
	def __init__( self, filename ):
		self._document = self._parse_doc( filename )
		super( DreamweaverPageParser, self ).__init__()
	
	@staticmethod
	def parse( filename ):
		page = DreamweaverTemplateInstance( filename=filename )
		return page
	
	@staticmethod
	def parse_doctitle( html, encoding=None ):
		defaults = {}
		if encoding:
			defaults['fromEncoding'] = encoding
		soup = BeautifulSoup( html, **defaults )
		elem = soup.find( 'title' )
		return "".join(elem.contents).strip()
	
	@staticmethod
	def parse_first_h1( html, encoding=None  ):
		defaults = {}
		if encoding:
			defaults['fromEncoding'] = encoding
		soup = BeautifulSoup( html, **defaults )
		elem = soup.find( 'h1' )
		if elem:
			return "".join(elem.contents).strip()
		else:
			return None
		
		
		
		

		