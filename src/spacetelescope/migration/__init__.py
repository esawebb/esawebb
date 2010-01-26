# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from parser import *
from django.contrib.redirects.models import Redirect
from djangoplicity.pages.models import Page

def nl2space( text ):
	if text:
		text = text.split('\n')
		text = [x.strip() for x in text]
		text = " ".join(text)
	return text

class Document( object ):
	"""
	Basic document for text files.
	"""
	parser = DocumentParser
	
	def __init__(self, filename ):
		self._filename = filename
		self._parse_doc() 
		self._title = None
		
	def _parse_doc(self):
		self._document = self.parser.parse( self._filename )
		
	def __unicode__( self ):
		return self.title()
	
	def title(self):
		return None
	
	def content(self):
		return self._document
	
	def description(self):
		return None
		
	def keywords(self):
		return None
	
	def section(self):
		return None

		
class SpacetelescopeDocument( Document ):
	"""
	"""
	parser = DreamweaverPageParser
	
	def _get_region(self, name ):
		if name in self._document.page_regions:
			return self._document.page_regions[name]
		else:
			return None
		
	def _clean_title(self,text):
		"""
		Remove unwanted boiler text from beginning of title.
		"""
		TITLE_PREPENDS = ["The European Homepage For The NASA/ESA Hubble Space Telescope -", "The European Homepage For The NASA/ESA Hubble Space Telescope"]
		for t in TITLE_PREPENDS: 
			if text.startswith( t ):
				text = text.replace( t, "" )
			
		return text.strip()
	
	def _doctitle(self):
		""" Extract doctitle from Dreamweaver template """
		html = self._get_region( "doctitle" )
		val = self.parser.parse_doctitle( html )
		val = self._clean_title( val )
		if val == "":
			return None
		return val
	
	def _content_h1(self):
		""" Extract doctitle from Dreamweaver template """
		html = self._get_region( "ContentArea" )
		val = self.parser.parse_first_h1( html )
		val = self._clean_title( val )
		if val == "":
			return None
		return val
	
	def _headline(self):
		""" Extract Headline region from Dreamweaver template """
		val = self._get_region( "Headline" )
		return nl2space(val)
	
	def title(self):
		""" Title of the document. """
		if not self._title:
			tmp = self._headline() # First try if there's a template title
			tmp = tmp if tmp else self._doctitle()
			self._title = tmp if tmp else self._content_h1() 
		return self._title
	
	
	def _document_content(self):
		pagecontent = self._get_region('PageContent')
		contentarea = self._get_region('ContentArea')
		  
		if pagecontent:
			headline = self._headline()
			if not headline:
				return pagecontent
			else:
				return "<h1>%s</h1>\n%s" % (headline,pagecontent)
		elif contentarea:
			return contentarea
		else:
			return None
		
	def _fix_links( self, text ):
		pass
		
	
	def content(self):
		content = self._document_content()
		
		return content
	
	def description(self):
		return None
		
	def keywords(self):
		return None
	
	def section(self):
		return None
	

class Migration( object ):
	"""
	Base class for any kind of migration
	"""
	def __init__( self, conf ):
		self.conf = conf
	
	def migrate(self):
		pass
	
	def set_state( self, state ):
		self._state = state
		
	def get_state( self ):
		return self._state
	
	state = property( fget=get_state, fset=set_state )
 

class PageMigrationInitialization( Migration ):
	"""
	"""
	def migrate(self):
		Page.objects.all().delete()
		Redirect.objects.all().delete()


class PageMigration( Migration ):
	"""
	Migration of a single document on the file path
	"""
	DEFAULT_PAGES = ['index.html','index.htm']
	
	def __init__( self, conf, filename=None, docclass=Document ):
		self._filename = filename
		self._docclass = docclass
		super( PageMigration, self ).__init__( conf )

	def filepath(self):
		"""
		Get absolute path to file for document
		"""
		return os.path.join( self.conf['root'], self._filename )
		
	def new_url(self):
		"""
		Generate new URL for page.
		"""
		elements = list(os.path.split( self._filename ))
		filename = elements[-1]
		
		if elements[0] == '':
			del elements[0]
		
		if filename in self.DEFAULT_PAGES:
			return '/%s/' % "/".join( elements[:-1] )
		else:
			base,ext = os.path.splitext( filename )
			elements[-1] = base
			return '/%s/' % "/".join( elements )
		
	def old_urls(self):
		"""
		Determine URLs of old document 
		"""
		elements = os.path.split( self._filename )
		if elements[-1] in self.DEFAULT_PAGES:
			return ["/%s" % self._filename,'/%s/' % "/".join( elements[:-1] ) ]
		else: 
			return ["/%s" % self._filename]
		
	def setup_redirects(self, old_urls, new_url ):
		"""
		Setup redirects for new URLs
		"""
		for url in old_urls:
			if url != new_url:
				r = Redirect( site=self.conf['default_site'], old_path=url, new_path=new_url )
				r.save()
	

	def migrate(self):
		"""
		Migrate document
		"""
		document = self._docclass( self.filepath() )
		new_url = self.new_url()
		
		
		#
		# Create page object
		# 
		p = Page( 
				title=document.title(),
				url=new_url,
				content=document.content(),
				section=self.conf['default_section'],
			)
		p.save()
		
		#
		# Create redirects
		#
		self.setup_redirects( self.old_urls(), new_url )
		
		#
		# Update global state
		#
		
		# save p id, extracted links.
		