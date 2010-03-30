# coding: utf-8
#
# Djangoplicity
# Copyright 2008 ESA/Hubble & International Astronomical Union
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import os
from PIL import Image as PILImage
from datetime import datetime, time
from django import forms
from django.conf.urls.defaults import *
from django.core.urlresolvers import NoReverseMatch, reverse
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from djangoplicity.archives import ArchiveOptions
from djangoplicity.archives.contrib import security
from djangoplicity.archives.contrib.browsers import *
from djangoplicity.archives.contrib.info import *
from djangoplicity.archives.contrib.queries import AllPublicQuery, UnpublishedQuery, YearQuery, EmbargoQuery, StagingQuery
from djangoplicity.archives.importer.forms import GenericImportForm
from djangoplicity.templatetags.djangoplicity_datetime import datetime as datetime_format
from djangoplicity.metadata.archives.info import *
from models import *


def release_date( obj ):
	print 
	if obj.release_date:
		if obj.release_date.time() == time(0,0):
			return datetime_format( obj.release_date, arg='DATE' )
		else:
			return datetime_format( obj.release_date, arg='DATETIME' )
	else:
		return None

#__all__ = ('EducationalMaterialOptions', 
#		   )
#	( _(u'Logos'), {'resources' : ( 'png', 'eps', 'illustrator', 'illustrator_text', ), 'icons' : { 'png' : 'phot', 'eps' : 'phot', 'illustrator' : 'phot', 'illustrator_text' : 'phot'} } ),
		
		
#TODO: nice strings

class StandardOptions (ArchiveOptions):
	"""
	Defines common options across all ST archives	
	"""		

	admin = (
		( _(u'Admin'), { 'links' : ( admin_edit_for_site('admin_site'),  ), 'fields' : ( published, 'release_date', 'last_modified', 'created', priority ), }  ),
	)
	
	search_fields = ( 
		'id', 'title', 'description', 'credit',
	)
	
	#TODO
	#feeds = {
	#	'' :	get_latest_images_class(),
	#	'category' : get_latest_images_class(), 
	#}
		
	#TODO
	#import_form = ImageImportForm
	
	class Browsers(object):
		normal = NormalBrowser( index_template='archives/index_normal.html', paginate_by=16 )
		viewall = ViewAllBrowser( index_template='archives/index_viewall.html', paginate_by=100 )
		
	#class ResourceProtection (object):
	#	unpublished = (UnpublishedQuery,security.UNPUBLISHED_PERMS)
	#	staging = (StagingQuery,security.STAGING_PERMS)
	#	embargo = (EmbargoQuery,security.EMBARGO)
		
	@staticmethod
	def queryset( request, model ):
		"""
		Query set for detail view. Make sure we select related objects right away,
		as we need the later on.
		"""
		return model._default_manager.all()
	
	#@staticmethod
	#def handle_import( obj, id=None, file_path=None, title=None, priority=None, published=None, wallpapers=None, zoomify=None, **kwargs ):


	


	

	
